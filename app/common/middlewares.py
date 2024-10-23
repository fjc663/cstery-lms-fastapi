from fastapi import Request, Header, status
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JOSEError
import fnmatch  # 用于路径匹配

from starlette.responses import JSONResponse

from app.config.authConfig import TEACHER_INCLUDE_PATHS, TEACHER_EXCLUDE_PATHS, STUDENT_EXCLUDE_PATHS, STUDENT_INCLUDE_PATHS
from app.config.jwtConfig import SECRET_KEY, ALGORITHM
from app.constant.jwtConstant import TEACHER_ID, STUDENT_ID
from app.common.result import Result


# 定义一个依赖，用于获取请求头中的 Authorization token
async def get_token_header(token: str = Header(None, description='登录校验令牌')):
    return token


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 验证教师端路径
        if self._is_protected_path(path, TEACHER_INCLUDE_PATHS, TEACHER_EXCLUDE_PATHS):
            validation_response = await self._validate_token(request, TEACHER_ID)
            if validation_response:  # 如果有验证失败的响应，直接返回该响应
                return validation_response

        # 验证学生端路径
        if self._is_protected_path(path, STUDENT_INCLUDE_PATHS, STUDENT_EXCLUDE_PATHS):
            validation_response = await self._validate_token(request, STUDENT_ID)
            if validation_response:  # 如果有验证失败的响应，直接返回该响应
                return validation_response

        response = await call_next(request)
        return response

    @staticmethod
    def _is_protected_path(path: str, include_paths: list, exclude_paths: list) -> bool:
        # 判断是否在排除路径中
        for pattern in exclude_paths:
            if fnmatch.fnmatch(path, pattern):
                return False

        # 判断是否在拦截路径中
        for pattern in include_paths:
            if fnmatch.fnmatch(path, pattern):
                return True

        return False

    @staticmethod
    async def _validate_token(request: Request, id_type: str):
        # 从请求中提取Token
        token = request.headers.get("token")
        if not token:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=Result.error(0, "未提供Token").dict())

        try:
            # 验证Token并获取用户信息
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get(id_type)
            if user_id is None:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=Result.error(0, "无效Token").dict())
            request.state.user_id = user_id  # 将用户ID存储在请求状态中
        except ExpiredSignatureError:
            # 处理Token过期错误
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=Result.error(0, "Token已过期").dict())
        except JOSEError:
            # 处理其他JWT错误
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=Result.error(0, "无效Token").dict())

        # 如果验证通过则返回 None，继续处理请求
        return None

from fastapi import APIRouter, Request

from app.common.enums import RoleEnum
from app.service import userService
from app.common.result import Result
from app.models.baseModels.userBaseModel import UserModel, LoginModel, RegisterModel

student_user_api = APIRouter()


@student_user_api.post("/login", summary="学生登录")
async def use_login(login_model: LoginModel):
    token = await userService.login(login_model, RoleEnum.STUDENT)
    return Result.success(token)


@student_user_api.post("/register", summary="学生注册")
async def add(register_model: RegisterModel):
    await userService.register(register_model, RoleEnum.STUDENT)
    return Result.success()


@student_user_api.get("", summary="返回当前学生信息")
async def get_user_info(request: Request):
    current_user_id = request.state.user_id  # 从请求中获取用户ID
    user = await userService.get_user_info(current_user_id)
    return Result.success(user)


@student_user_api.put("", summary="更新学生信息")
async def update_user_info(user: UserModel, request: Request):
    current_user_id = request.state.user_id  # 从请求中获取用户ID
    await userService.update(user, current_user_id)
    return Result.success()

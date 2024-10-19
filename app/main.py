import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from apis import teacher_user_api, student_user_api
from app.settings import TORTOISE_ORM
from app.common.result import Result
from app.common.middlewares import AuthMiddleware, get_token_header

app = FastAPI(dependencies=[Depends(get_token_header)])

# 配置 SQL 日志打印 （调试时可开启查看具体的sql执行）
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("tortoise")
# logger.setLevel(logging.DEBUG)

register_tortoise(
    app=app,
    config=TORTOISE_ORM
)

app.add_middleware(AuthMiddleware)


# 捕获全局其它异常
@app.exception_handler(Exception)
async def other_exception_handler(_, __):
    return JSONResponse(status_code=500, content=Result.error(msg="未知异常").dict())


# 捕获全局业务异常
@app.exception_handler(HTTPException)
async def service_exception_handler(_, ex: HTTPException):
    return JSONResponse(status_code=ex.status_code, content=Result.error(msg=ex.detail).dict())

app.include_router(teacher_user_api, prefix='/teacher/user', tags=["教师端用户相关接口"])
app.include_router(student_user_api, prefix='/student/user', tags=["学生端用户相关接口"])

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True, log_level="debug")

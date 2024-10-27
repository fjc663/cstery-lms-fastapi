import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise
from apis import teacher_user_api, student_user_api
from app.apis.common.deleteFileApi import delete_file_api
from app.apis.common.uploadFileApi import upload_file_api
from app.apis.student.studentClassApi import student_class_api
from app.apis.student.studentTaskApi import student_task_api
from app.apis.teacher.teacherClassApi import teacher_class_api
from app.apis.teacher.teacherReportApi import teacher_report_api
from app.apis.teacher.teacherTaskApi import teacher_task_api
from app.common.exceptions import LmsBaseException
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
    config=TORTOISE_ORM,

)

# 挂载静态文件
app.mount("/avatar", StaticFiles(directory="../static/avatar"))
app.mount("/class", StaticFiles(directory="../static/class"))
app.mount("/imgs", StaticFiles(directory="../static/imgs"))

# 注册中间件
app.add_middleware(AuthMiddleware)


# 捕获全局其它异常
@app.exception_handler(Exception)
async def other_exception_handler(_, __):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=Result.error(msg="未知异常").dict())


# 捕获全局业务异常
@app.exception_handler(LmsBaseException)
async def service_exception_handler(_, ex: HTTPException):
    return JSONResponse(status_code=ex.status_code, content=Result.error(msg=ex.detail).dict())


app.include_router(teacher_user_api, prefix='/teacher/user', tags=["教师端用户相关接口"])
app.include_router(teacher_class_api, prefix='/teacher/class', tags=["教师端班级相关接口"])
app.include_router(teacher_task_api, prefix='/teacher/task', tags=["教师端作业相关接口"])
app.include_router(teacher_report_api, prefix='/teacher/report', tags=["教师端成绩报告相关接口"])

app.include_router(student_user_api, prefix='/student/user', tags=["学生端用户相关接口"])
app.include_router(student_class_api, prefix='/student/class', tags=["学生端班级相关接口"])
app.include_router(student_task_api, prefix='/student/task', tags=["学生端作业相关接口"])

app.include_router(upload_file_api, prefix='/upload', tags=["文件上传相关接口"])
app.include_router(delete_file_api, prefix='/delete', tags=["文件删除相关接口"])

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True, log_level="debug")

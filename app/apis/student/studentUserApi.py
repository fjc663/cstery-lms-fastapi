from fastapi import APIRouter, Request

from app.service import studentService
from app.common.result import Result
from app.models.baseModels.userBaseModel import StudentModel, LoginModel, RegisterModel, EditPasswordModel

student_user_api = APIRouter()


@student_user_api.post("/login", summary="学生登录")
async def student_login(login_model: LoginModel):
    token_and_avatar = await studentService.student_login(login_model)
    return Result.success(token_and_avatar)


@student_user_api.post("/register", summary="学生注册")
async def student_register(register_model: RegisterModel):
    await studentService.student_register(register_model)
    return Result.success()


@student_user_api.get("", summary="返回当前学生信息")
async def get_student_info(request: Request):
    current_student_id = request.state.user_id  # 从请求中获取用户ID
    student = await studentService.get_student_info(current_student_id)
    return Result.success(student)


@student_user_api.put("", summary="更新学生信息")
async def update_student_info(user: StudentModel, request: Request):
    current_student_id = request.state.user_id  # 从请求中获取用户ID
    await studentService.student_update(user, current_student_id)
    return Result.success()


@student_user_api.put("/editPassword", summary="修改密码")
async def update_teacher_password(password_model: EditPasswordModel, request: Request):
    student_id = request.state.user_id  # 从请求中获取用户ID
    await studentService.update_student_password(password_model, student_id)
    return Result.success()
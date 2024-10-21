from fastapi import APIRouter, Request

from app.service import teacherService
from app.common.result import Result
from app.models.baseModels.userBaseModel import TeacherModel, LoginModel, RegisterModel

teacher_user_api = APIRouter()


@teacher_user_api.post("/login", summary="教师登录")
async def teacher_login(login_model: LoginModel):
    token_and_avatar = await teacherService.teacher_login(login_model)
    return Result.success(token_and_avatar)


@teacher_user_api.post("/register", summary="教师注册")
async def teacher_register(register_model: RegisterModel):
    await teacherService.teacher_register(register_model)
    return Result.success()


@teacher_user_api.get("", summary="返回当前教师信息")
async def get_teacher_info(request: Request):
    current_teacher_id = request.state.user_id  # 从请求中获取用户ID
    teacher = await teacherService.get_teacher_info(current_teacher_id)
    return Result.success(teacher)


@teacher_user_api.put("", summary="更新教师信息")
async def update_teacher_info(user: TeacherModel, request: Request):
    current_teacher_id = request.state.user_id  # 从请求中获取用户ID
    await teacherService.teacher_update(user, current_teacher_id)
    return Result.success()

#
# @user_api.get("/page", summary="分页查询用户信息")
# async def get_user_page(page_query: UserPageQueryModel = Query(..., description="分页查询条件")):
#     page_result = await userService.get_user_page(page_query)
#     return Result.success(page_result)
#
#
# @user_api.delete("", summary="根据id删除用户")
# async def delete_user_info(user_id: int):
#     await userService.delete(user_id)
#     return Result.success()

from fastapi import APIRouter, Request

from app.common.enums import RoleEnum
from app.service import userService
from app.common.result import Result
from app.models.baseModels.userBaseModel import UserModel, LoginModel, RegisterModel

teacher_user_api = APIRouter()


@teacher_user_api.post("/login", summary="教师登录")
async def use_login(login_model: LoginModel):
    token = await userService.login(login_model, RoleEnum.TEACHER)
    return Result.success(token)


@teacher_user_api.post("/register", summary="教师注册")
async def add(register_model: RegisterModel):
    await userService.register(register_model, RoleEnum.TEACHER)
    return Result.success()


@teacher_user_api.get("", summary="返回当前教师信息")
async def get_user_info(request: Request):
    current_user_id = request.state.user_id  # 从请求中获取用户ID
    user = await userService.get_user_info(current_user_id)
    return Result.success(user)


@teacher_user_api.put("", summary="更新教师信息")
async def update_user_info(user: UserModel, request: Request):
    current_user_id = request.state.user_id  # 从请求中获取用户ID
    await userService.update(user, current_user_id)
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

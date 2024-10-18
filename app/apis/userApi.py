from fastapi import APIRouter, Request, Query
from app.service import userService
from app.result import Result
from app.baseModels import UserModel, LoginModel, UserPageQueryModel

user_api = APIRouter()


@user_api.post("/login", summary="管理员登录")
async def use_login(login_model: LoginModel):
    token = await userService.login(login_model)
    return Result.success(token)


@user_api.post("", summary="管理员添加用户")
async def add(user: UserModel):
    await userService.register(user)
    return Result.success()


@user_api.get("", summary="获得当前用户信息")
async def get_user_info(request: Request):
    current_user_id = request.state.user_id  # 从请求中获取用户ID
    user = await userService.get_user_info(current_user_id)
    return Result.success(user)


@user_api.put("", summary="更新用户信息")
async def update_user_info(user: UserModel):
    await userService.update(user)
    return Result.success()


@user_api.get("/page", summary="分页查询用户信息")
async def get_user_page(page_query: UserPageQueryModel = Query(..., description="分页查询条件")):
    page_result = await userService.get_user_page(page_query)
    return Result.success(page_result)


@user_api.delete("", summary="根据id删除用户")
async def delete_user_info(user_id: int):
    await userService.delete(user_id)
    return Result.success()

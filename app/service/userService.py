from fastapi import status, HTTPException
from tortoise.exceptions import DoesNotExist
from app.baseModels import UserModel, LoginModel, UserPageQueryModel
from app.constant.jwtConstant import ADMIN_ID
from app.result import PageResult
from app.utils import get_password_hash, verify_password, create_access_token
from app.models import User
from datetime import datetime
from app.exceptions import UserException


# 用户登录
async def login(login_model: LoginModel):
    """
    用户登录
    :param login_model: 登录表单
    :return: JWT令牌
    """
    try:
        # 尝试获取用户信息
        user = await User.get(username=login_model.username)
    except DoesNotExist:
        # 如果用户不存在，抛出 404 错误
        raise UserException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    # 验证密码
    if not verify_password(login_model.password, user.password):
        # 如果密码不匹配，抛出 401 错误
        raise UserException(status_code=status.HTTP_401_UNAUTHORIZED, detail="密码错误")

    # 生成 JWT token
    data = {ADMIN_ID: user.id}
    token = create_access_token(data)
    return {'token': token, 'id': user.id}


# 用户注册
async def register(user_model: UserModel):
    """
    用户注册
    :param user_model: 用户表单
    :return:
    """

    # 判断用户名和密码是否有效
    if user_model.username is None or user_model.password is None:
        raise UserException(status_code=status.HTTP_400_BAD_REQUEST, detail="请输入正确的用户名和密码")

    # 默认为用户角色
    if user_model.role is None:
        user_model.role = "user"

    # 加密密码
    user_model.password = get_password_hash(user_model.password)

    user = user_model.dict(exclude_none=True)
    user["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await User.create(**user)


# 请求当前用户信息
async def get_user_info(current_user_id: int):
    user = await User.get(id=current_user_id)
    user.password = "******"
    return user


# 更新用户信息
async def update(user_model: UserModel):
    user = user_model.dict(exclude_none=True)
    user_id = user.pop("id")

    await User.filter(id=user_id).update(**user)


# 分页查询用户信息
async def get_user_page(page_query: UserPageQueryModel):
    query = User.all()

    # 过滤条件
    if page_query.username:
        query = query.filter(username__icontains=page_query.username)

    if page_query.role:
        query = query.filter(role__icontains=page_query.role)

    if page_query.phone:
        query = query.filter(phone__icontains=page_query.phone)

    if page_query.place:
        query = query.filter(place__icontains=page_query.place)

    if page_query.address:
        query = query.filter(address__icontains=page_query.address)

    if page_query.remark:
        query = query.filter(remark__icontains=page_query.remark)

    total = await query.count()

    records = await query.offset((page_query.page - 1) * page_query.pageSize).limit(page_query.pageSize)

    return PageResult(total=total, records=records)


# 根据id删除用户
async def delete(user_id):
    deleted_count = await User.filter(id=user_id).delete()

    if deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户未找到")

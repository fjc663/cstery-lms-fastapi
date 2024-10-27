from typing import Union

from fastapi import status
from tortoise.exceptions import DoesNotExist

from app.common.enums import GenderEnum
from app.models.baseModels.userBaseModel import StudentModel, LoginModel, RegisterModel, TeacherModel, UserInfo, \
    EditPasswordModel
from app.utils import get_password_hash, verify_password, create_access_token
from datetime import datetime
from app.common.exceptions import UserException
from app.utils.validUtil import validate_username, validate_password


# 用户登录
async def login(login_model: LoginModel, model, token_id: str):
    """
    用户登录
    :param login_model: 登录表单
    :param model: ORM模型
    :param token_id: token对应的键值
    :return: JWT令牌和头像URL
    """
    try:
        # 尝试获取用户信息
        user = await model.get(username=login_model.username)
    except DoesNotExist:
        # 如果用户不存在，抛出 404 错误
        raise UserException(status_code=status.HTTP_200_OK, detail="用户不存在")

    # 验证密码
    if not verify_password(login_model.password, user.password):
        # 如果密码不匹配，抛出 401 错误
        raise UserException(status_code=status.HTTP_200_OK, detail="密码错误")

    # 生成 JWT token
    data = {token_id : user.id}
    token = create_access_token(data)

    return UserInfo(token=token, avatar=user.avatar, name=user.name)


# 用户注册
async def register(register_model: RegisterModel, model):
    """
    用户注册
    :param register_model: 注册表单
    :param model: ORM模型
    :return:
    """

    # 判断用户名是否重复
    try:
        await model.get(username=register_model.username)
        raise UserException(status_code=status.HTTP_200_OK, detail="用户名已存在")
    except DoesNotExist:
        # 用户不存在，可以继续注册流程
        pass

    user = register_model.model_dump(exclude_none=True)

    # 判断密码和确认密码是否相同
    confirm_password = user.pop('confirm_password', None)
    if confirm_password:
        if confirm_password != user.get('password'):
            raise UserException(status_code=status.HTTP_200_OK, detail="密码和确认密码不相同")

    # 校验用户名和密码格式
    validate_username(user['username'])
    validate_password(user['password'])

    # 加密密码
    user['password'] = get_password_hash(user['password'])

    user["avatar"] = 'http://127.0.0.1:8080/avatar/defaultAvatar.png' # 默认头像
    user["gender"] = GenderEnum.OTHER
    user["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await model.create(**user)


# 请求当前用户信息
async def get_user_info(current_user_id: int, model):
    # 查询用户信息
    user = await model.get(id=current_user_id)

    user = vars(user)
    user.pop('password', None)  # 删除密码字段

    return user


# 更新用户信息
async def update(base_model: Union[TeacherModel, StudentModel], model, user_id: int):
    user = base_model.model_dump(exclude_none=True)
    user["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 尝试更新用户信息
    updated_count = await model.filter(id=user_id).update(**user)

    if updated_count == 0:
        # 没有找到用户
        raise UserException(status_code=status.HTTP_200_OK, detail="用户不存在")


# 更新用户头像
async def update_avatar(model, avatar: str, user_id: int):
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 更新
    count = await model.filter(id=user_id).update(avatar=avatar, updated_at=updated_at)

    # 判断是否更新成功
    if count == 0:
        raise UserException(status_code=status.HTTP_200_OK, detail="修改失败")


# 修改用户密码
async def update_password(model, password_model: EditPasswordModel, user_id: int):
    try:
        # 尝试获取用户信息
        user = await model.get(id=user_id)
    except DoesNotExist:
        # 如果用户不存在，抛出 404 错误
        raise UserException(status_code=status.HTTP_200_OK, detail="用户不存在")

    # 验证密码
    if not verify_password(password_model.old_password, user.password):
        # 如果密码不匹配，抛出 401 错误
        raise UserException(status_code=status.HTTP_200_OK, detail="密码错误")

    # 判断密码和确认密码是否相同
    if password_model.confirm_password != password_model.new_password:
        raise UserException(status_code=status.HTTP_200_OK, detail="密码和确认密码不相同")

    # 校验密码格式
    validate_password(password_model.new_password)

    # 加密密码
    hash_new_password = get_password_hash(password_model.new_password)

    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 修改密码
    count = await model.filter(id=user_id).update(password=hash_new_password, updated_at=updated_at)

    if count == 0:
        raise UserException(status_code=status.HTTP_200_OK, detail="修改错误")


# # 分页查询用户信息
# async def get_user_page(page_query: UserPageQueryModel):
#     query = User.all()
#
#     # 过滤条件
#     if page_query.username:
#         query = query.filter(username__icontains=page_query.username)
#
#     if page_query.role:
#         query = query.filter(role__icontains=page_query.role)
#
#     if page_query.phone:
#         query = query.filter(phone__icontains=page_query.phone)
#
#     if page_query.place:
#         query = query.filter(place__icontains=page_query.place)
#
#     if page_query.address:
#         query = query.filter(address__icontains=page_query.address)
#
#     if page_query.remark:
#         query = query.filter(remark__icontains=page_query.remark)
#
#     total = await query.count()
#
#     records = await query.offset((page_query.page - 1) * page_query.pageSize).limit(page_query.pageSize)
#
#     return PageResult(total=total, records=records)
#
#
# # 根据id删除用户
# async def delete(user_id):
#     deleted_count = await User.filter(id=user_id).delete()
#
#     if deleted_count == 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户未找到")

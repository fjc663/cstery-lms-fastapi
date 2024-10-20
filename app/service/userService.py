from fastapi import status
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.common.enums import RoleEnum
from app.models.baseModels.userBaseModel import UserModel, LoginModel, RegisterModel
from app.constant.jwtConstant import TEACHER_ID, STUDENT_ID
from app.utils import get_password_hash, verify_password, create_access_token
from app.models.models import User
from datetime import datetime
from app.common.exceptions import UserException


# 用户登录
async def login(login_model: LoginModel, role: RoleEnum):
    """
    用户登录
    :param role: 登录的用户角色
    :param login_model: 登录表单
    :return: JWT令牌
    """
    try:
        # 尝试获取用户信息
        user = await User.get(username=login_model.username)
    except DoesNotExist:
        # 如果用户不存在，抛出 404 错误
        raise UserException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    # 判断用户角色是否在对应系统登陆(学生、教师、管理)
    if user.role != role:
        raise UserException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="请到{}端登录".format(
                                '学生' if user.role == RoleEnum.STUDENT else
                                '教师' if user.role == RoleEnum.TEACHER else
                                '管理'
                            ))

    # 验证密码
    if not verify_password(login_model.password, user.password):
        # 如果密码不匹配，抛出 401 错误
        raise UserException(status_code=status.HTTP_401_UNAUTHORIZED, detail="密码错误")

    # 生成 JWT token
    data = {TEACHER_ID if user.role == RoleEnum.TEACHER else STUDENT_ID : user.id}
    token = create_access_token(data)
    return token


# 用户注册
async def register(register_model: RegisterModel, role: RoleEnum):
    """
    用户注册
    :param role: 注册的用户角色
    :param register_model: 注册表单
    :return:
    """

    # 判断用户名是否重复
    try:
        await User.get(username=register_model.username)
        raise UserException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    except DoesNotExist:
        # 用户不存在，可以继续注册流程
        pass

    user = register_model.model_dump(exclude_none=True)

    # 判断密码和确认密码是否相同
    confirm_password = user.pop('confirm_password', None)
    if confirm_password:
        if confirm_password != user.get('password'):
            raise UserException(status_code=status.HTTP_400_BAD_REQUEST, detail="密码和确认密码不相同")

    # 加密密码
    user['password'] = get_password_hash(user['password'])

    user["role"] = role.value
    user["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await User.create(**user)


# 请求当前用户信息
async def get_user_info(current_user_id: int):
    user = await User.get(id=current_user_id)
    user.password = "******"
    return user


# 更新用户信息
async def update(user_model: UserModel, user_id: int):
    user = user_model.model_dump(exclude_none=True)
    user["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # 尝试更新用户信息
        updated_count = await User.filter(id=user_id).update(**user)

        if updated_count == 0:
            # 如果没有找到用户，返回 404
            raise UserException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    except IntegrityError as e:
        # 捕获唯一约束异常
        if "Duplicate entry" in str(e):
            raise UserException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
        else:
            # 处理其他 IntegrityError 错误
            raise UserException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="数据库错误")

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

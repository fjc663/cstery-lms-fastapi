from app.models.baseModels.userBaseModel import TeacherModel, LoginModel, RegisterModel
from app.constant.jwtConstant import TEACHER_ID
from app.service import userService
from app.models.models import Teacher


# 教师登录
async def teacher_login(login_model: LoginModel):
    """
    教师登录
    :param login_model: 登录表单
    :return: JWT令牌和头像URL
    """

    return await userService.login(login_model=login_model, model=Teacher, token_id=TEACHER_ID)


# 教师注册
async def teacher_register(register_model: RegisterModel):
    """
    教师注册
    :param register_model: 注册表单
    :return:
    """

    await userService.register(register_model=register_model, model=Teacher)


# 请求当前用户信息
async def get_teacher_info(current_teacher_id: int):
    return await userService.get_user_info(current_user_id=current_teacher_id, model=Teacher)


# 更新用户信息
async def teacher_update(teacher_model: TeacherModel, teacher_id: int):
    await userService.update(base_model=teacher_model, model=Teacher, user_id=teacher_id)

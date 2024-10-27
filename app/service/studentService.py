from app.models.baseModels.userBaseModel import StudentModel, LoginModel, RegisterModel
from app.constant.jwtConstant import STUDENT_ID
from app.service import userService
from app.models.models import Student


# 学生登录
async def student_login(login_model: LoginModel):
    """
    学生登录
    :param login_model: 登录表单
    :return: JWT令牌
    """

    return await userService.login(login_model=login_model, model=Student, token_id=STUDENT_ID)


# 学生注册
async def student_register(register_model: RegisterModel):
    """
    学生注册
    :param register_model: 注册表单
    :return:
    """

    await userService.register(register_model=register_model, model=Student)


# 请求当前用户信息
async def get_student_info(current_student_id: int):
    return await userService.get_user_info(current_user_id=current_student_id, model=Student)


# 更新用户信息
async def student_update(student_model: StudentModel, student_id: int):
    await userService.update(base_model=student_model, model=Student, user_id=student_id)


# 更新头像
async def update_student_avatar(avatar: str, student_id: int):
    await userService.update_avatar(model=Student, avatar=avatar, user_id=student_id)


# 修改密码
async def update_student_password(password_model, student_id):
    await userService.update_password(model=Student, password_model=password_model, user_id=student_id)

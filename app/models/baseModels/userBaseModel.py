from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from app.common.enums import GenderEnum


# 登录模型
class LoginModel(BaseModel):
    username: Optional[str] = Field(..., description="用户名")
    password: Optional[str] = Field(..., description="密码")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "fjc663",
                "password": "123456",
            }
        }

# 注册模型
class RegisterModel(BaseModel):
    username: Optional[str] = Field(None, description="用户名", min_length=1, max_length=20)
    password: Optional[str] = Field(None, description="密码", min_length=6, max_length=18)
    confirm_password: Optional[str] = Field(..., description="确认密码", min_length=6, max_length=18)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "fjc663",
                "password": "123456",
                "confirm_password": "123456",
            }
        }

# 用户信息模型
class UserModel(BaseModel):
    username: Optional[str] = Field(None, description="用户名", min_length=1, max_length=20)
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    gender: Optional[GenderEnum] = Field(GenderEnum.OTHER.value, description="性别")
    phone: Optional[str] = Field(None, description="手机号码", pattern=r'^\+?[1-9]\d{1,14}$')
    address: Optional[str] = Field(None, description="住址")
    desc: Optional[str] = Field(None, description="用户描述信息")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "fjc663",
                "email": "johndoe@example.com",
                "gender": GenderEnum.MALE.value,
                "phone": "1234567890",
                "address": "123 Elm Street, Springfield",
                "desc": "A passionate teacher and tech enthusiast.",
            }
        }

# 用户信息分页查询
# class UserPageQueryModel(BaseModel):
#     page: int
#     pageSize: int
#     username: Optional[str] = None
#     role: Optional[str] = None
#     phone: Optional[str] = None
#     place: Optional[str] = None
#     address: Optional[str] = None
#     remark: Optional[str] = None


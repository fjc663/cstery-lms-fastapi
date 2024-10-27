from datetime import datetime
from typing import Optional, Any
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
    username: Optional[str] = Field(
        ...,
        description="用户名",
        min_length=1,
        max_length=20,
    )
    password: Optional[str] = Field(
        ...,
        description="密码",
        min_length=6,
        max_length=18,
    )
    confirm_password: Optional[str] = Field(
        ...,
        description="确认密码",
        min_length=6,
        max_length=18,
    )

    class Config:
        json_schema_extra = {
            "example": {
                "username": "fjc663",
                "password": "123456",
                "confirm_password": "123456",
            }
        }


# 教师信息模型
class TeacherModel(BaseModel):
    name: Optional[str] = Field(None, description="姓名")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    gender: Optional[GenderEnum] = Field(GenderEnum.OTHER.value, description="性别")
    phone: Optional[str] = Field(None, description="手机号码", pattern=r'^\+?[1-9]\d{1,14}$')
    birthdate: Optional[datetime] = Field(None, description="出生日期")
    address: Optional[str] = Field(None, description="住址")
    desc: Optional[str] = Field(None, description="用户描述信息")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "fjc663",
                "name": "李老师",
                "email": "johndoe@example.com",
                "gender": GenderEnum.MALE.value,
                "phone": "1234567890",
                "address": "123 Elm Street, Springfield",
                "desc": "A passionate teacher and tech enthusiast.",
            }
        }


# 学生信息模型
class StudentModel(BaseModel):
    name: Optional[str] = Field(None, description="姓名")
    student_number: Optional[str] = Field(None, description="学号")
    school: Optional[str] = Field(None, description="学校名")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    gender: Optional[GenderEnum] = Field(GenderEnum.OTHER.value, description="性别")
    phone: Optional[str] = Field(None, description="手机号码", pattern=r'^\+?[1-9]\d{1,14}$')
    birthdate: Optional[datetime] = Field(None, description="出生日期")
    address: Optional[str] = Field(None, description="住址")
    desc: Optional[str] = Field(None, description="用户描述信息")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "fjc663",
                "name": "张三",
                "student_number": "3128004455",
                "school": "广工某大学",
                "email": "johndoe@example.com",
                "gender": GenderEnum.MALE.value,
                "phone": "1234567890",
                "address": "123 Elm Street, Springfield",
                "desc": "A passionate teacher and tech enthusiast.",
            }
        }


# 学生信息分页查询
class StudentPageQueryModel(BaseModel):
    page: int = Field(..., description="页码")
    pageSize: int = Field(..., description="每页学生数")
    name: Optional[str] = Field(None, description="姓名")
    gender: Optional[int] = Field(None, description="性别")

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "pageSize": 10,
                "name": "张三",
                "gender": GenderEnum.MALE.value
            }
        }


# 登录后后返回的用户信息模型
class UserInfo:
    token: str
    avatar: str
    name: str

    def __init__(self, token: str, avatar: str, name: str):
        self.token = token
        self.avatar = avatar
        self.name = name


# 修改密码模型
class EditPasswordModel(BaseModel):
    old_password: Optional[str] = Field(
        ...,
        description="旧密码",
        min_length=6,
        max_length=18,
    )
    new_password: Optional[str] = Field(
        ...,
        description="新密码",
        min_length=6,
        max_length=18,
    )
    confirm_password: Optional[str] = Field(
        ...,
        description="确认密码",
        min_length=6,
        max_length=18,
    )

    class Config:
        json_schema_extra = {
            "example": {
                "old_password": "123456",
                "new_password": "654321",
                "confirm_password": "654321",
            }
        }
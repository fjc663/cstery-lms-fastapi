from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator


# 登录模型
class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "cstery667",
                "password": "123456",
            }
        }


# 用户信息模型
class UserModel(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    place: Optional[str] = None
    address: Optional[str] = None
    desc: Optional[str] = None
    remarks: Optional[str] = None
    avatar: Optional[str] = None

# 用户信息分页查询
class UserPageQueryModel(BaseModel):
    page: int
    pageSize: int
    username: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    place: Optional[str] = None
    address: Optional[str] = None
    remark: Optional[str] = None


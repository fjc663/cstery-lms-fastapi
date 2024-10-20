from typing import Optional

from pydantic import BaseModel, Field


# 班级模型
class ClassModel(BaseModel):
    id: Optional[int] = Field(None, description="班级ID")
    class_name: Optional[str] = Field(..., min_length=1, max_length=100)
    desc: Optional[str] = Field(None, description="班级描述信息")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "class_name": "2024秋季软件工程",
                "desc": "学习软件开发流程"
            }
        }
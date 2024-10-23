from typing import Optional

from pydantic import BaseModel, Field


# 班级模型
class ClassModel(BaseModel):
    id: Optional[int] = Field(None, description="班级ID")
    class_name: Optional[str] = Field(..., min_length=1, max_length=100)
    teacher_name: Optional[str] = Field(None, min_length=1, max_length=100)
    class_img: Optional[str] = Field(None)
    desc: Optional[str] = Field(None, description="班级描述信息")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "class_name": "2024秋季软件工程",
                "teacher_name": "赵老师",
                "class_img": "http://127.0.0.1:8080/class/class_img.png",
                "desc": "学习软件开发流程"
            }
        }

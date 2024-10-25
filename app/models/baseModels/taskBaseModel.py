from typing import Optional, List

from pydantic import BaseModel, Field


# 作业提交模型
class TaskModel(BaseModel):
    title: Optional[str] = Field(..., min_length=1, max_length=100, description="作业解答标题")
    desc: Optional[str] = Field(None, description="作业解答描述")
    images: Optional[List[str]] = Field(None, description="作业解答图片列表")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "软件工程第一次作业",
                "desc": "开发流程：项目需求 -> 分析需求 -> 搭建项目结构 -> 开发 -> ...",
                "images": [
                    "http://127.0.0.1:8080/task/task1.png",
                    "http://127.0.0.1:8080/task/task2.png",
                    "http://127.0.0.1:8080/task/task3.png"
                ]
            }
        }

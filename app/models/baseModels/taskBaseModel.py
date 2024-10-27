from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.common.enums import FormatEnum


# 答案提交模型
class AnswerModel(BaseModel):
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


# 作业模型
class TaskModel(BaseModel):
    id: Optional[int] = Field(None, description="作业ID")
    title: str = Field(..., min_length=1, max_length=200, description="作业标题")
    desc: Optional[str] = Field(None, description="作业描述")
    due_date: Optional[datetime] = Field(None, description="作业截止日期")
    allow_late_submission: bool = Field(False, description="是否允许迟交")
    submission_format: FormatEnum = Field(..., description="提交格式，如 'text', 'img'")
    clas_id: int = Field(..., description="所属班级 ID")
    images: Optional[List[str]] = Field(None, description="作业图片列表")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "软件工程第一次作业",
                "desc": "开发流程：项目需求 -> 分析需求 -> 搭建项目结构 -> 开发 -> ...",
                "due_date": "2024-12-31T23:59:59",
                "allow_late_submission": False,
                "submission_format": "text",
                "clas_id": 101,
                "images": [
                    "http://127.0.0.1:8080/task/task1.png",
                    "http://127.0.0.1:8080/task/task2.png",
                    "http://127.0.0.1:8080/task/task3.png"
                ]
            }
        }


# 作业批改模型
class CorrectModel(BaseModel):
    student_id: int = Field(..., description="学生 ID")
    task_id: int = Field(..., description="作业 ID")
    score: int = Field(..., description="作业分数")
    feedback: Optional[str] = Field(None, description="教师反馈")

    class Config:
        json_schema_extra = {
            "example": {
                "student_id": 2,
                "task_id": 1,
                "score": 90,
                "feedback": "完成得很好，下次就继续努力。"
            }
        }


# 学生信息分页查询
class TaskPageQueryModel(BaseModel):
    page: int = Field(..., description="页码")
    pageSize: int = Field(..., description="每页学生数")
    task_title: Optional[str] = Field(None, description="作业标题")
    class_name: Optional[str] = Field(None, description="班级名称")
    is_cut_off: Optional[bool] = Field(None, description="是否截止")

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "pageSize": 10,
                "task_title": "软件工程第一次作业",
                "class_name": "2024软件工程计科",
                "is_cut_off": True
            }
        }
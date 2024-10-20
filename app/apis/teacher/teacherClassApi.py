from fastapi import APIRouter
from fastapi.params import Query
from starlette.requests import Request

from app.common.result import Result
from app.models.baseModels.classBaseModel import ClassModel
from app.service import classService

teacher_class_api = APIRouter()


@teacher_class_api.post("", summary="创建班级")
async def create_class(class_model: ClassModel, request: Request):
    teacher_id = request.state.user_id  # 从请求中获取用户ID
    await classService.create_class(class_model, teacher_id)
    return Result.success()


@teacher_class_api.put("", summary="修改班级信息")
async def update_class(class_model: ClassModel):
    await classService.update_class(class_model)
    return Result.success()


@teacher_class_api.get("", summary="返回当前教师所创建的班级")
async def get_class(request: Request):
    teacher_id = request.state.user_id
    class_list = await classService.get_class(teacher_id)
    return Result.success(class_list)

@teacher_class_api.delete("", summary="删除班级")
async def delete_class(class_id: int = Query(..., description="班级ID")):
    await classService.delete_class(class_id)
    return Result.success()

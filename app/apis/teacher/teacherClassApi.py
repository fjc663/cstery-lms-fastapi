from fastapi import APIRouter
from fastapi.params import Query
from starlette.requests import Request

from app.common.result import Result
from app.models.baseModels.classBaseModel import ClassModel
from app.models.baseModels.userBaseModel import StudentPageQueryModel
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
    class_list = await classService.get_class_by_teacher_id(teacher_id)
    return Result.success(class_list)

@teacher_class_api.delete("", summary="删除班级")
async def delete_class(class_id: int = Query(..., description="班级ID")):
    await classService.delete_class(class_id)
    return Result.success()


@teacher_class_api.get("/stu/{class_id}", summary="获得班级学生信息")
async def get_class_stu(class_id: int, request: Request):
    teacher_id = request.state.user_id
    students = await classService.get_class_stu(class_id, teacher_id)
    return Result.success(students)


@teacher_class_api.get("/{class_id}", summary="获得班级详细信息")
async def get_class_by_id(class_id: int):
    clas = await classService.get_class_by_id(class_id)
    return Result.success(clas)


@teacher_class_api.get("/stu/page/{class_id}", summary="分页查询班级学生信息")
async def get_user_page(class_id: int, request: Request, page_query_model: StudentPageQueryModel = Query(..., description="分页查询条件")):
    teacher_id = request.state.user_id
    page_result = await classService.get_student_page(page_query_model,class_id, teacher_id)
    return Result.success(page_result)
from fastapi import APIRouter, Request, Query

from app.common.result import Result
from app.service import classService

student_class_api = APIRouter()


@student_class_api.post("/join", summary="加入班级")
async def join_class(request: Request,
                     class_code: str = Query(..., description="班级邀请码")):
    student_id = request.state.user_id
    await classService.join_class(student_id, class_code)
    return Result.success()


@student_class_api.post("/exit", summary="退出班级")
async def exit_class(request: Request,
                     class_code: str = Query(..., description="班级邀请码")):
    student_id = request.state.user_id
    await classService.exit_class(student_id, class_code)
    return Result.success()


@student_class_api.get("", summary="查询已加入的班级")
async def get_class_by_student_id(request: Request):
    student_id = request.state.user_id
    classes = await classService.get_class_by_student_id(student_id)
    return Result.success(classes)


@student_class_api.get("/code", summary="根据邀请码查询班级信息")
async def get_class_by_code(class_code: str = Query(..., description="班级邀请码")):
    clas = await classService.get_class_by_code(class_code)
    return Result.success(clas)


@student_class_api.get("/{class_id}", summary="获得班级详细信息")
async def get_class_by_id(class_id: int):
    clas = await classService.get_class_by_id(class_id)
    return Result.success(clas)

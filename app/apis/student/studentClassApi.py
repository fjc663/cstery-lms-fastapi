from fastapi import APIRouter, Request, Form

from app.common.result import Result
from app.service import classService

student_class_api = APIRouter()


@student_class_api.post("/join", summary="加入班级")
async def join_class(request: Request,
                     class_code: str = Form(...,
                                            min_length=8,
                                            max_length=8,
                                            description="班级邀请码")):
    student_id = request.state.user_id
    await classService.join_class(student_id, class_code)
    return Result.success()


@student_class_api.post("/exit", summary="退出班级")
async def exit_class(request: Request,
                     class_code: str = Form(...,
                                            min_length=8,
                                            max_length=8,
                                            description="班级邀请码")):
    student_id = request.state.user_id
    await classService.exit_class(student_id, class_code)
    return Result.success()


@student_class_api.get("", summary="查询已加入的班级")
async def get_class(request: Request):
    student_id = request.state.user_id
    classes = await classService.get_class_by_student_id(student_id)
    return Result.success(classes)
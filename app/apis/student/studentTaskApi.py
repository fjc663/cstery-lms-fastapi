from fastapi import APIRouter, Request

from app.common.result import Result
from app.models.baseModels.taskBaseModel import TaskModel
from app.service import taskService

student_task_api = APIRouter()


@student_task_api.get("/class/{class_id}", summary="根据班级ID获得班级作业信息")
async def get_task_by_class_id(class_id: int, request: Request):
    student_id = request.state.user_id
    tasks = await taskService.get_task_by_class_id(class_id, student_id)
    return Result.success(tasks)


@student_task_api.get("/{task_id}", summary="根据ID返回作业信息")
async def get_task_by_id(task_id: int, request: Request):
    student_id = request.state.user_id
    task = await taskService.get_task_by_id(task_id, student_id)
    return Result.success(task)


@student_task_api.get("/answer/{task_id}", summary="根据作业ID和学生ID返回作业作答信息")
async def get_answer_by_id(task_id: int, request: Request):
    student_id = request.state.user_id
    task = await taskService.get_answer_by_id(task_id, student_id)
    return Result.success(task)


@student_task_api.post("/{task_id}", summary="提交作业")
async def submit_task(task_id: int, task_mode: TaskModel, request: Request):
    student_id = request.state.user_id
    await taskService.submit_task(task_id, task_mode, student_id)
    return Result.success()


@student_task_api.put("/{task_id}", summary="修改作业")
async def edit_task(task_id: int, task_mode: TaskModel, request: Request):
    student_id = request.state.user_id
    await taskService.edit_task(task_id, task_mode, student_id)
    return Result.success()
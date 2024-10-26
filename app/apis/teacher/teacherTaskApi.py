from fastapi import APIRouter, Query

from app.common.result import Result
from app.models.baseModels.taskBaseModel import TaskModel, CorrectModel
from app.service import taskService

teacher_task_api = APIRouter()


@teacher_task_api.post("", summary="创建作业")
async def create_task(task_mode: TaskModel):
    await taskService.create_task(task_mode)
    return Result.success()


@teacher_task_api.get("/{task_id}", summary="根据ID返回作业信息")
async def get_task_by_id(task_id: int):
    task = await taskService.get_task_by_id(task_id)
    return Result.success(task)


@teacher_task_api.get("/completion/{task_id}", summary="根据作业ID返回完成情况")
async def get_task_completion(task_id: int):
    task_completion = await taskService.get_task_completion(task_id)
    return Result.success(task_completion)


@teacher_task_api.put("", summary="修改作业")
async def edit_task(task_mode: TaskModel):
    await taskService.edit_task(task_mode)
    return Result.success()


@teacher_task_api.get("/answer/{student_id}", summary="根据学生ID和作业ID返回作答信息")
async def get_answer(student_id: int, task_id: int = Query(..., description="作业ID")):
    answer = await taskService.get_answer(student_id, task_id)
    return Result.success(answer)


@teacher_task_api.put("/correct", summary="根据学生ID和作业ID批改作业")
async def correct_task(correct_model: CorrectModel):
    await taskService.correct_task(correct_model)
    return Result.success()
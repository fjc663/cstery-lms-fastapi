from fastapi import APIRouter, Request, Query

from app.common.result import Result
from app.models.baseModels.taskBaseModel import TaskPageQueryModel
from app.service import reportService

teacher_report_api = APIRouter()

@teacher_report_api.get('', summary='返回所有作业完成情况')
async def get_all_task(request: Request, page_query_model: TaskPageQueryModel = Query(..., description="分页条件")):
    teacher_id = request.state.user_id
    tasks = await reportService.get_all_task(teacher_id=teacher_id, page_query_model=page_query_model)
    return Result.success(tasks)


@teacher_report_api.get('/{task_id}', summary='根据ID返回作业完成情况')
async def get_task_report(task_id: int):
    task_report = await reportService.get_task_report(task_id=task_id)
    return Result.success(task_report)

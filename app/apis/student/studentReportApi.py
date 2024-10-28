from fastapi import APIRouter, Request, Query

from app.common.result import Result
from app.models.baseModels.taskBaseModel import TaskPageQueryModel
from app.service import reportService

student_report_api = APIRouter()

@student_report_api.get('', summary='分页查询作业完成情况')
async def student_page_query_task(request: Request, page_query_model: TaskPageQueryModel = Query(..., description="分页条件")):
    student_id = request.state.user_id
    tasks = await reportService.student_page_query_task(student_id=student_id, page_query_model=page_query_model)
    return Result.success(tasks)


@student_report_api.get('/chart', summary='返回学生作业完成情况的图表数据')
async def get_chart_data(request: Request):
    student_id = request.state.user_id
    chart_data = await reportService.get_chart_data(student_id=student_id)
    return Result.success(chart_data)
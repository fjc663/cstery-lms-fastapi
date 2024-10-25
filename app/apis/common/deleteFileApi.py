from typing import List

from fastapi import APIRouter, Query

from app.common.result import Result
from app.utils import uploadUtil

delete_file_api = APIRouter()


@delete_file_api.delete("/student/task", summary="作业图片删除")
async def task_image_delete(filenames: List[str] = Query(..., description='要删除图片的文件名')):
    await rename_and_delete(filenames, "student/task")
    return Result.success()


async def rename_and_delete(filenames, prefix):
    for filename in filenames:
        new_filename = f"{prefix}/{filename}"
        uploadUtil.delete_file(new_filename)




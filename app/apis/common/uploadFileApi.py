import uuid

from fastapi import APIRouter, UploadFile, File

from app.common.result import Result
from app.utils import uploadUtil

upload_file_api = APIRouter()


@upload_file_api.post("/teacher/avatar", summary="头像上传")
async def avatar_upload(avatar_file: UploadFile = File(...)):
    path = await rename_and_upload(avatar_file, "avatar/teacher")
    return Result.success(path)


@upload_file_api.post("/teacher/class", summary="班级图片上传")
async def class_image_upload(class_image_file: UploadFile = File(...)):
    path = await rename_and_upload(class_image_file, "class/teacher")
    return Result.success(path)


@upload_file_api.post("/student/task", summary="作业图片上传")
async def task_image_upload(task_image_file: UploadFile = File(...)):
    path = await rename_and_upload(task_image_file, "student/task")
    return Result.success(path)


async def rename_and_upload(file, prefix):
    file_extension = file.filename.split(".")[-1]
    new_filename = f"{prefix}/{uuid.uuid4()}.{file_extension}"
    file_data = await file.read()

    return uploadUtil.upload_file(file_data, new_filename)

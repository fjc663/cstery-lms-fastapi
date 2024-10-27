import uuid

from fastapi import APIRouter, UploadFile, File, Request

from app.common.result import Result
from app.service import teacherService
from app.utils import uploadUtil

upload_file_api = APIRouter()


@upload_file_api.post("/teacher/avatar", summary="头像上传")
async def avatar_upload(request: Request, avatar_file: UploadFile = File(...)):
    path = await rename_and_upload(avatar_file, "teacher/avatar")

    teacher_id = request.state.user_id
    # 更新数据库
    await teacherService.update_teacher_avatar(avatar=path, teacher_id=teacher_id)

    return Result.success(path)


@upload_file_api.post("/teacher/class", summary="班级图片上传")
async def class_image_upload(class_image_file: UploadFile = File(...)):
    path = await rename_and_upload(class_image_file, "teacher/class")
    return Result.success(path)


@upload_file_api.post("/student/answer", summary="作业答案图片上传")
async def answer_image_upload(answer_image_file: UploadFile = File(...)):
    path = await rename_and_upload(answer_image_file, "student/answer")
    return Result.success(path)


@upload_file_api.post("/teacher/task", summary="作业图片上传")
async def task_image_upload(task_image_file: UploadFile = File(...)):
    path = await rename_and_upload(task_image_file, "teacher/task")
    return Result.success(path)


async def rename_and_upload(file, prefix):
    file_extension = file.filename.split(".")[-1]
    new_filename = f"{prefix}/{uuid.uuid4()}.{file_extension}"
    file_data = await file.read()

    return uploadUtil.upload_file(file_data, new_filename)

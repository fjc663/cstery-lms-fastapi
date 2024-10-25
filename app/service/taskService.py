from datetime import datetime

from app.common.exceptions import TaskException
from app.models.baseModels.taskBaseModel import TaskModel
from app.models.models import Assignment, ClassStudent, Class, StudentAssignment
from fastapi import status
from tortoise.exceptions import DoesNotExist


# 根据班级ID和学生ID获得班级作业信息
async def get_task_by_class_id(class_id, student_id: int):
    # 判断班级是否存在
    try:
        await Class.get(id=class_id)
    except DoesNotExist:
        raise TaskException(status_code=status.HTTP_200_OK, detail="班级不存在")

    # 判断是否为本班学生
    try:
        await ClassStudent.get(clas_id=class_id, student_id=student_id)
    except DoesNotExist:
        raise TaskException(status_code=status.HTTP_200_OK, detail="非本班学生无法查询")

    # 查询学生作业关联表
    student_tasks = await StudentAssignment.filter(student_id=student_id)

    # 已提交作业的ID列表
    task_ids = [student_task.assignment_id for student_task in student_tasks]

    # 查询班级作业
    tasks = await Assignment.filter(clas_id=class_id, is_deleted=False).order_by('created_at')

    # 添加 `submitted` 字段表示学生是否提交作业
    tasks_with_submitted = []
    for task in tasks:
        task = vars(task)
        if task.get('id') in task_ids:
            task['submitted'] = True
        else:
            task['submitted'] = False

        tasks_with_submitted.append(task)

    return tasks_with_submitted


# 根据ID返回作业信息
async def get_task_by_id(task_id: int, student_id: int):
    try:
        # 查询作业信息
        task = await Assignment.get(id=task_id)

        # 查询学生作业关联表
        student_task = await StudentAssignment.filter(assignment_id=task_id, student_id=student_id).first()

        # 判断是否提交过
        task = vars(task)
        if student_task:
            task['submitted'] = True
            # 设置最后一次提交的时间
            task['updated_at'] = student_task.updated_at
        else:
            task['submitted'] = False

    except DoesNotExist:
        raise TaskException(status_code=status.HTTP_200_OK, detail="作业不存在")

    return task


# 根据作业ID和学生ID返回作业作答信息
def get_answer_by_id(task_id, student_id):
    answer = StudentAssignment.filter(assignment_id=task_id, student_id=student_id).first()

    return answer


# 提交作业
async def submit_task(task_id: int, task_model: TaskModel, student_id: int):
    # 判断是不是重复提交
    student_assignment = await StudentAssignment.filter(assignment_id=task_id, student_id=student_id).first()
    if student_assignment:
        raise TaskException(status_code=status.HTTP_200_OK, detail="请不要重复提交")

    # 去除为None的字段
    task_model = task_model.model_dump(exclude_none=True)

    # 校验作业是否存在
    try:
        task = await Assignment.get(id=task_id)

        # 判断是否到截止时间和不允许提交
        if datetime.now() > datetime.combine(task.due_date, datetime.max.time()) and not task.allow_late_submission:
            raise TaskException(status_code=status.HTTP_200_OK, detail="已截至，无法提交")

        # 校验是否需要图片
        if task.submission_format == "img" and task_model.get('images') is None:
            raise TaskException(status_code=status.HTTP_200_OK, detail="请提交至少一张作业图片")

    except DoesNotExist:
        raise TaskException(status_code=status.HTTP_200_OK, detail="作业不存在")

    # 设置学生和作业信息
    task_model['assignment_id'] = task_id
    task_model['student_id'] = student_id
    task_model['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task_model['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 插入数据
    await StudentAssignment.create(**task_model)


# 修改作业
async def edit_task(task_id: int, task_model: TaskModel, student_id: int):
    # 去除为None的字段
    task_model = task_model.model_dump(exclude_none=True)

    # 校验作业是否存在
    try:
        task = await Assignment.get(id=task_id)

        # 判断是否到截止时间和不允许修改
        if datetime.now() > datetime.combine(task.due_date, datetime.max.time()) and not task.allow_late_submission:
            raise TaskException(status_code=status.HTTP_200_OK, detail="已截至，无法修改")

        # 校验是否需要图片
        if task.submission_format == "img" and task_model.get('images') is None:
            raise TaskException(status_code=status.HTTP_200_OK, detail="请提交至少一张作业图片")

    except DoesNotExist:
        raise TaskException(status_code=status.HTTP_200_OK, detail="作业不存在")

    # 设置学生和作业信息
    task_model['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 插入数据
    await StudentAssignment.filter(assignment_id=task_id, student_id=student_id).update(**task_model)

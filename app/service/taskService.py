from datetime import datetime
from typing import Optional

from app.common.exceptions import TaskException
from app.models.baseModels.taskBaseModel import AnswerModel, TaskModel, CorrectModel
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
async def get_task_by_id(task_id: int, student_id: Optional[int] = None):
    try:
        # 查询作业信息
        task = await Assignment.get(id=task_id)

        if student_id:
            # 查询学生作业关联表
            student_task = await StudentAssignment.filter(assignment_id=task_id, student_id=student_id).first()

            # 判断是否提交过
            task = vars(task)
            if student_task:
                task['submitted'] = True

                # 作业评分和教师评价
                task['score'] = student_task.score
                task['feedback'] = student_task.feedback
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
async def submit_task(task_id: int, answer_model: AnswerModel, student_id: int):
    # 判断是不是重复提交
    student_assignment = await StudentAssignment.filter(assignment_id=task_id, student_id=student_id).first()
    if student_assignment:
        raise TaskException(status_code=status.HTTP_200_OK, detail="请不要重复提交")

    # 去除为None的字段
    answer_model = answer_model.model_dump(exclude_none=True)

    # 校验作业是否存在
    try:
        task = await Assignment.get(id=task_id)

        # 判断是否到截止时间和不允许提交
        if task.due_date and datetime.now() > datetime.combine(task.due_date,
                                                               datetime.max.time()) and not task.allow_late_submission:
            raise TaskException(status_code=status.HTTP_200_OK, detail="已截至，无法提交")

        # 校验是否需要图片
        if task.submission_format == "img" and answer_model.get('images') is None:
            raise TaskException(status_code=status.HTTP_200_OK, detail="请提交至少一张作业图片")

    except DoesNotExist:
        raise TaskException(status_code=status.HTTP_200_OK, detail="作业不存在")

    # 设置学生和作业信息
    answer_model['assignment_id'] = task_id
    answer_model['student_id'] = student_id
    answer_model['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    answer_model['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 插入数据
    await StudentAssignment.create(**answer_model)


# 修改作业作答
async def edit_answer(task_id: int, answer_model: AnswerModel, student_id: int):
    # 去除为None的字段
    answer_model = answer_model.model_dump(exclude_none=True)

    # 校验作业是否存在
    try:
        task = await Assignment.get(id=task_id)

        # 判断是否到截止时间和不允许修改
        if task.due_date and datetime.now() > datetime.combine(task.due_date,
                                                               datetime.max.time()) and not task.allow_late_submission:
            raise TaskException(status_code=status.HTTP_200_OK, detail="已截至，无法修改")

        # 校验是否需要图片
        if task.submission_format == "img" and answer_model.get('images') is None:
            raise TaskException(status_code=status.HTTP_200_OK, detail="请提交至少一张作业图片")

    except DoesNotExist:
        raise TaskException(status_code=status.HTTP_200_OK, detail="作业不存在")

    # 设置学生和作业信息
    answer_model['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 插入数据
    await StudentAssignment.filter(assignment_id=task_id, student_id=student_id).update(**answer_model)


# 创建作业
async def create_task(task_mode: TaskModel):
    # 校验数据
    valid_data(task_mode)

    # 判断班级是否存在
    clas = await Class.filter(id=task_mode.clas_id)
    if not clas:
        raise TaskException(status_code=status.HTTP_200_OK, detail='班级不存在')

    # 去除None字段
    task_mode = task_mode.model_dump(exclude_none=True)

    # 增加创建和更新时间字段
    task_mode['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    task_mode['update_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 插入
    await Assignment.create(**task_mode)


# 根据作业ID返回完成情况
async def get_task_completion(task_id: int):
    try:
        # 根据作业ID查询作业
        task = await Assignment.get(id=task_id)

        # 根据班级id查询学生
        class_student_list = await ClassStudent.filter(clas_id=task.clas_id).prefetch_related("student")

        # 根据作业ID查询学生作业关联表，获得已完成作业学生的ID
        student_assignments = await StudentAssignment.filter(assignment_id=task_id).prefetch_related("student")
        student_completion_ids = [student_assignment.student_id for student_assignment in student_assignments]

        completion_status = {'submitted': [], 'not_submitted': []}
        # 设置提交列表
        for student_assignment in student_assignments:
            student = student_assignment.student
            student = vars(student)  # 转化为字典格式

            # 设置提交时间和修改时间信息
            student['submitted_at'] = student_assignment.created_at
            student['edited_at'] = student_assignment.updated_at
            student['is_correct'] = True if student_assignment.score else False

            completion_status['submitted'].append(student)

        # 设置未提交列表
        for class_student in class_student_list:
            if class_student.student.id not in student_completion_ids:
                completion_status['not_submitted'].append(class_student.student)

    except DoesNotExist:
        raise TaskException(status_code=status.HTTP_200_OK, detail="作业不存在")

    return completion_status


# 修改作业
async def edit_task(task_mode: TaskModel):
    # 校验数据
    valid_data(task_mode)

    # 去除None字段
    task_mode = task_mode.model_dump(exclude_none=True)

    # 增加创建和更新时间字段
    task_mode['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 去除ID字段
    task_id = task_mode.pop('id')

    # 更新
    count = await Assignment.filter(id=task_id).update(**task_mode)

    # 判断是否更新失败
    if count == 0:
        raise TaskException(status_code=status.HTTP_200_OK, detail="修改失败，请稍后尝试")


# 校验数据
def valid_data(task_mode: TaskModel):
    if task_mode.title is None or len(task_mode.title) == 0:
        raise TaskException(status_code=status.HTTP_200_OK, detail="请设置标题")
    if (task_mode.desc is None or len(task_mode.desc) == 0) and (
            task_mode.images is None or len(task_mode.images) == 0):
        raise TaskException(status_code=status.HTTP_200_OK, detail="请设置答题要求")


# 根据学生ID和作业ID返回作答信息
async def get_answer(student_id, task_id):
    try:
        answer = await StudentAssignment.get(student_id=student_id, assignment_id=task_id)
        student = await answer.student

        # 设置学生信息字段
        answer = vars(answer)
        answer['student_name'] = student.name
        answer['student_number'] = student.student_number

    except:
        raise TaskException(status_code=status.HTTP_200_OK, detail="作答不存在")

    return answer


# 根据学生ID和作业ID批改作业
async def correct_task(correct_model: CorrectModel):
    try:
        answer = StudentAssignment.filter(student_id=correct_model.student_id, assignment_id=correct_model.task_id)

        # 去除None字段并转化为字典类型
        correct_model = correct_model.model_dump(exclude_none=True)
        correct_model.pop('student_id')
        correct_model.pop('task_id')

        # 更新
        await answer.update(**correct_model)

    except:
        raise TaskException(status_code=status.HTTP_200_OK, detail="作答不存在")

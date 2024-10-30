from datetime import datetime, timedelta

from app.common.result import PageResult
from app.models.baseModels.taskBaseModel import TaskPageQueryModel
from app.models.models import Class, Assignment, ClassStudent, StudentAssignment, HomeImage
from app.service.taskService import get_task_completion


# 根据教师ID返回所有作业
async def get_all_task(teacher_id: int, page_query_model: TaskPageQueryModel):
    # 根据教师ID查询所有班级
    classes = await Class.filter(teacher_id=teacher_id, is_deleted=False)
    # 获取所有班级ID
    class_ids = [clas.id for clas in classes]

    # 根据班级IDS查询所有作业
    query = Assignment.filter(clas_id__in=class_ids, is_deleted=False)

    # 根据分页条件筛选
    if page_query_model.task_title:
        query = query.filter(title__icontains=page_query_model.task_title)
    if page_query_model.class_name:
        query = query.filter(clas__class_name__icontains=page_query_model.class_name)
    if page_query_model.is_cut_off is not None:
        if page_query_model.is_cut_off:
            query = query.filter(due_date__lt=datetime.now() - timedelta(days=1))
        else:
            query = query.filter(due_date__gt=datetime.now() - timedelta(days=1))

    # 数据总条数
    total = await query.count()
    # 查询
    tasks = await query.offset((page_query_model.page - 1) * page_query_model.pageSize).limit(
        page_query_model.pageSize)

    # 设置班级名称、完成人数、未完成人数、完成率、平均分字段
    new_tasks = []
    for task in tasks:
        # 获作业完成情况
        completion_status = await get_task_completion(task.id)

        # 设置班级名称、完成人数、未完成人数、总人数、完成率字段
        clas = await task.clas
        class_name = clas.class_name
        task = vars(task)
        task['class_name'] = class_name
        task['completed_count'] = len(completion_status['submitted'])
        task['not_completed_count'] = len(completion_status['not_submitted'])
        task['total_count'] = len(completion_status['submitted']) + len(completion_status['not_submitted'])
        task['completion_rate'] = task['completed_count'] / task['total_count'] if task['completed_count'] else 0

        # 设置平均分字段
        correct_count = 0  # 已批改数量
        score = 0  # 全部分数之和
        for correct in completion_status['submitted']:
            if correct['score']:
                correct_count += 1
                score += correct['score']
        average_score = score / correct_count if correct_count else 0
        task['average_score'] = average_score

        new_tasks.append(task)

    return PageResult(total=total, records=new_tasks)


# 根据ID返回作业完成情况
async def get_task_report(task_id):
    # 获作业完成情况
    completion_status = await get_task_completion(task_id)

    # 根据作业ID查询作业
    task = await Assignment.get(id=task_id, is_deleted=False)

    # 设置完成人数、未完成人数
    task = vars(task)
    task['completed_count'] = len(completion_status['submitted'])
    task['not_completed_count'] = len(completion_status['not_submitted'])

    # 设置平均分、及格率字段、各分数段人数
    correct_count = 0  # 已批改数量
    score = 0  # 全部分数之和
    gt60_count = 0  # 及格人数
    score_list = [0 for _ in range(5)]
    for correct in completion_status['submitted']:
        if correct['score'] is not None:
            correct_count += 1
            score += correct['score']
            if correct['score'] >= 60:
                gt60_count += 1

            # 各分数段统计
            if 0 <= correct['score'] < 60:
                score_list[0] += 1
            elif 60 <= correct['score'] < 70:
                score_list[1] += 1
            elif 70 <= correct['score'] < 80:
                score_list[2] += 1
            elif 80 <= correct['score'] < 90:
                score_list[3] += 1
            elif 90 <= correct['score'] <= 100:
                score_list[4] += 1

    average_score = score / correct_count if correct_count else 0
    pass_rate = gt60_count / correct_count if correct_count else 0

    task['average_score'] = average_score
    task['pass_rate'] = pass_rate
    task['score_list'] = score_list

    return task


# 学生端分页查询作业情况
async def student_page_query_task(student_id, page_query_model):
    # 根据学生ID查询所有提交的作业
    query = StudentAssignment.filter(student_id=student_id, assignment__is_deleted=False).prefetch_related('assignment')

    # 根据分页条件筛选
    if page_query_model.task_title:
        query = query.filter(assignment__title__icontains=page_query_model.task_title)
    if page_query_model.class_name:
        query = query.filter(assignment__clas__class_name__icontains=page_query_model.class_name)
    if page_query_model.is_cut_off is not None:
        if page_query_model.is_cut_off:
            query = query.filter(assignment__due_date__lt=datetime.now() - timedelta(days=1))
        else:
            query = query.filter(assignment__due_date__gt=datetime.now() - timedelta(days=1))

    # 数据总条数
    total = await query.count()
    # 查询
    answers = await query.offset((page_query_model.page - 1) * page_query_model.pageSize).limit(
        page_query_model.pageSize)

    # 设返回信息
    task_reports = []
    for answer in answers:
        task_report = {}

        task_report['task_id'] = answer.assignment_id
        task_report['task_title'] = answer.assignment.title
        clas = await answer.assignment.clas
        task_report['class_name'] = clas.class_name
        task_report['due_date'] = answer.assignment.due_date
        task_report['score'] = answer.score

        task_reports.append(task_report)

    return PageResult(total=total, records=task_reports)


# 返回学生作业完成情况的图表数据
async def get_chart_data(student_id):
    # 根据学生ID查询所有提交的作业
    student_assignments = await StudentAssignment.filter(student_id=student_id, assignment__is_deleted=False)

    # 提取分数列表
    score_list = [0 for _ in range(5)]
    for student_assignment in student_assignments:
        if student_assignment.score is not None:
            # 各分数段统计
            if 0 <= student_assignment.score < 60:
                score_list[0] += 1
            elif 60 <= student_assignment.score < 70:
                score_list[1] += 1
            elif 70 <= student_assignment.score < 80:
                score_list[2] += 1
            elif 80 <= student_assignment.score < 90:
                score_list[3] += 1
            elif 90 <= student_assignment.score <= 100:
                score_list[4] += 1

    # 完成的作业数
    completion_count = len(student_assignments)

    # 获得加入的班级ids
    class_students = await ClassStudent.filter(student_id=student_id, clas__is_deleted=False)
    class_ids = [class_student.clas_id for class_student in class_students]

    # 查询所有作业数
    tasks = await Assignment.filter(clas_id__in=class_ids, is_deleted=False)

    # 未完成的作业数
    not_completion_count = len(tasks)

    # 图表数据
    chart_data = {
        'completion_count': completion_count,
        'not_completion_count': not_completion_count,
        'score_list': score_list
    }

    return chart_data


# 返回首页图片
async def get_home_image(is_stu: bool):
    images = await HomeImage.filter(is_stu=is_stu)

    return images
from datetime import datetime, timedelta

from app.common.result import PageResult
from app.models.baseModels.taskBaseModel import TaskPageQueryModel
from app.models.models import Class, Assignment
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
        correct_count = 0 # 已批改数量
        score = 0 # 全部分数之和
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
    correct_count = 0 # 已批改数量
    score = 0 # 全部分数之和
    gt60_count = 0 # 及格人数
    score_list = [0 for _ in range(5)]
    for correct in completion_status['submitted']:
        if correct['score']:
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

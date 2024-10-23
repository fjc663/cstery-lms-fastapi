from tortoise.transactions import atomic

from app.common.enums import GenderEnum
from app.common.exceptions import ClassException
from app.common.result import PageResult
from app.models.baseModels.classBaseModel import ClassModel
from app.models.baseModels.userBaseModel import StudentPageQueryModel
from app.models.models import Class, ClassStudent, Teacher
from app.utils.classUtil import generate_class_code
from datetime import datetime
from tortoise.exceptions import DoesNotExist
from fastapi import status


# 创建班级
@atomic()
async def create_class(class_model: ClassModel, teacher_id: int):
    clas = class_model.model_dump(exclude_none=True)

    # 设置班级信息
    clas['class_code'] = generate_class_code(teacher_id)
    clas['teacher_id'] = teacher_id
    clas['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    clas['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 插入班级数据
    await Class.create(**clas)


# 修改班级信息
@atomic()
async def update_class(class_model: ClassModel):
    clas = class_model.model_dump(exclude_none=True)

    class_id = clas.pop('id')

    # 更新
    await Class.filter(id=class_id).update(**clas)


# 根据教师ID返回班级信息
async def get_class_by_teacher_id(teacher_id: int):
    # 查询该教师所有班级信息
    classes = await Class.filter(teacher_id=teacher_id, is_deleted=False)
    # 查询当前教师信息
    teacher = await Teacher.get(id=teacher_id)

    # 去除 'teacher_id' 字段，添加 'teacher_name' 字段
    teacher_name = teacher.name if teacher.name else teacher.username
    for clas in classes:
        clas = vars(clas)
        clas.pop('teacher_id')
        if not clas['teacher_name']:
            clas['teacher_name'] = teacher_name

    return classes


# 删除班级
@atomic()
async def delete_class(class_id: int):
    # 判断班级是否存在
    try:
        clas: Class = await Class.get(id=class_id)
    except DoesNotExist:
        raise ClassException(status_code=status.HTTP_404_NOT_FOUND, detail="班级不存在")

    # 判断是否已删除
    if clas.is_deleted:
        raise ClassException(status_code=status.HTTP_400_BAD_REQUEST, detail="班级已删除，请勿重复操作")

    # 逻辑删除班级信息
    await Class.filter(id=class_id).update(is_deleted=True)


# 根据班级码加入班级
@atomic()
async def join_class(student_id, class_code):
    try:
        clas = await Class.get(class_code=class_code, is_deleted=False)
    except DoesNotExist:
        raise ClassException(status_code=status.HTTP_404_NOT_FOUND, detail="班级不存在")

    # 判断学生是否在班级
    try:
        await ClassStudent.get(clas_id=clas.id, student_id=student_id)
        raise ClassException(status_code=status.HTTP_404_NOT_FOUND, detail="已加入班级，请勿重复操作")
    except DoesNotExist:
        # 将学生加入班级
        await ClassStudent.create(
            clas_id=clas.id,
            student_id=student_id,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )


# 根据班级码退出班级
@atomic()
async def exit_class(student_id, class_code):
    try:
        clas = await Class.get(class_code=class_code, is_deleted=False)
    except DoesNotExist:
        raise ClassException(status_code=status.HTTP_404_NOT_FOUND, detail="班级不存在")

    await ClassStudent.filter(student_id=student_id, clas_id=clas.id).delete()


# 查询已加入的班级
async def get_class_by_student_id(student_id):
    # 查询学生班级关联表
    class_student_list = await ClassStudent.filter(student_id=student_id).prefetch_related("clas")

    # 返回班级对象列表
    return [class_student.clas for class_student in class_student_list]


# 根据班级ID查询学生信息
async def get_class_stu(class_id: int, teacher_id: int):
    # 判断该教师是否存在该班级
    try:
        await Class.get(id=class_id, teacher_id=teacher_id, is_deleted=False)
    except DoesNotExist:
        raise ClassException(status_code=status.HTTP_404_NOT_FOUND, detail="班级不存在")

    # 查询学生班级关联表
    class_student_list = await ClassStudent.filter(clas_id=class_id).prefetch_related("student")

    # 移除每个 student 对象中的 password 字段
    student_list = []
    for class_student in class_student_list:
        student_data = vars(class_student.student)
        student_data.pop('password', None)  # 删除密码字段
        student_list.append(student_data)

    # 返回班级学生列表
    return student_list


# 根据班级ID返回信息
async def get_class_by_id(class_id, teacher_id):
    # 根据班级ID和教师ID查询班级
    clas = await Class.get(id=class_id, teacher_id=teacher_id, is_deleted=False)
    # 查询当前教师信息
    teacher = await Teacher.get(id=teacher_id)

    # 去除 'teacher_id' 字段，添加 'teacher_name' 字段
    clas = vars(clas)
    clas.pop('teacher_id')
    if not clas['teacher_name']:
        teacher_name = teacher.name if teacher.name else teacher.username
        clas['teacher_name'] = teacher_name

    return clas


# 分页查询班级学生信息
async def get_student_page(page_query_model: StudentPageQueryModel, class_id: int, teacher_id: int):
    # 判断该教师是否存在该班级
    try:
        await Class.get(id=class_id, teacher_id=teacher_id, is_deleted=False)
    except DoesNotExist:
        raise ClassException(status_code=status.HTTP_404_NOT_FOUND, detail="班级不存在")

    # 查询该教师所有班级信息
    query = ClassStudent.filter(clas_id=class_id).prefetch_related("student")

    # 过滤条件
    if page_query_model.name:
        query = query.filter(student__name__icontains=page_query_model.name)
    if page_query_model.gender in [member.value for member in GenderEnum]:
        query = query.filter(student__gender=page_query_model.gender)

    # 数据总条数
    total = await query.count()
    # 查询
    students = await query.offset((page_query_model.page - 1) * page_query_model.pageSize).limit(page_query_model.pageSize)

    # 移除每个 student 对象中的 password 字段
    student_list = []
    for class_student in students:
        student_data = vars(class_student.student)
        student_data.pop('password', None)  # 删除密码字段
        student_list.append(student_data)


    return PageResult(total=total, records=student_list)


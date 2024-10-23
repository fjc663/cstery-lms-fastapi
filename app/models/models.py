from tortoise.models import Model
from tortoise import fields

from app.common.enums import GenderEnum


# 教师表
class Teacher(Model):
    id = fields.IntField(pk=True, description="主键ID")
    username = fields.CharField(max_length=100, description="用户名")
    password = fields.CharField(max_length=100, description="密码")
    name = fields.CharField(max_length=100, null=True, description="姓名")
    email = fields.CharField(max_length=100, null=True, description="教师的邮箱地址")
    gender = fields.IntEnumField(GenderEnum, description="用户性别: 0-女性, 1-男性, 2-保密")
    phone = fields.CharField(max_length=100, null=True, description="教师的联系电话")
    address = fields.CharField(max_length=100, null=True, description="教师的地址")
    desc = fields.TextField(null=True, description="教师的个人描述或介绍")
    avatar = fields.CharField(max_length=100, null=True, description="教师头像的URL")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "teacher"


# 用户表
class Student(Model):
    id = fields.IntField(pk=True, description="主键ID")
    username = fields.CharField(max_length=100, description="用户名")
    password = fields.CharField(max_length=100, description="密码")
    name = fields.CharField(max_length=100, null=True, description="姓名")
    student_number = fields.CharField(max_length=100, null=True, description="学号")
    school = fields.CharField(max_length=100, null=True, description="学校名称")
    email = fields.CharField(max_length=100, null=True, description="学生的邮箱地址")
    gender = fields.IntEnumField(GenderEnum, description="用户性别: 0-女性, 1-男性, 2-保密")
    phone = fields.CharField(max_length=100, null=True, description="学生的联系电话")
    address = fields.CharField(max_length=100, null=True, description="学生的地址")
    desc = fields.TextField(null=True, description="学生的个人描述或介绍")
    avatar = fields.CharField(max_length=100, null=True, description="学生头像的URL")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "student"


# 班级表
class Class(Model):
    id = fields.IntField(pk=True, description="班级的唯一标识符")
    class_name = fields.CharField(max_length=100, description="班级名称")
    class_code = fields.CharField(max_length=20, unique=True, description="班级邀请码")
    teacher_name = fields.CharField(max_length=100, null=True, description="老师名称")
    teacher = fields.ForeignKeyField("models.Teacher", related_name="classes", on_delete=fields.CASCADE,
                                     description="班级对应的教师")
    desc = fields.TextField(null=True, description="班级的详细描述")
    class_img = fields.CharField(max_length=255, null=True, description="班级图片的URL")
    created_at = fields.DatetimeField(auto_now_add=True, description="班级创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="班级最后更新时间")
    is_deleted = fields.BooleanField(default=False, description="是否删除")

    class Meta:
        table = "class"


# 班级学生关联表
class ClassStudent(Model):
    id = fields.IntField(pk=True, description="班级学生关系的唯一标识符")
    clas = fields.ForeignKeyField("models.Class", related_name="students", on_delete=fields.CASCADE, description="班级")
    student = fields.ForeignKeyField("models.Student", related_name="student_classes", on_delete=fields.CASCADE,
                                     description="学生")
    created_at = fields.DatetimeField(auto_now_add=True, description="学生加入时间")

    class Meta:
        table = "class_student"


# 任务表
class Assignment(Model):
    id = fields.IntField(pk=True, description="作业的唯一标识符")
    title = fields.CharField(max_length=200, description="作业标题")
    desc = fields.TextField(null=True, description="作业的详细描述")
    due_date = fields.DateField(null=True, description="作业截止日期")
    allow_late_submission = fields.BooleanField(default=False, description="是否允许截止后提交作业")
    submission_format = fields.CharField(max_length=50, null=True, default="text", description="作业提交的格式")
    images = fields.JSONField(null=True, description="作业图片的URL列表，以JSON格式存储")
    created_at = fields.DatetimeField(auto_now_add=True, description="作业创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="作业最后更新时间")

    class Meta:
        table = "assignment"


# 班级任务关联表
class ClassAssignment(Model):
    id = fields.IntField(pk=True, description="班级作业关系的唯一标识符")
    clas = fields.ForeignKeyField("models.Class", related_name="assignments", on_delete=fields.CASCADE,
                                  description="班级")
    assignment = fields.ForeignKeyField("models.Assignment", related_name="class_assignments", on_delete=fields.CASCADE,
                                        description="作业")
    assigned_at = fields.DatetimeField(auto_now_add=True, description="作业分配时间")

    class Meta:
        table = "class_assignment"

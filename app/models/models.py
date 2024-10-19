from tortoise.models import Model
from tortoise import fields

from app.common.enums import RoleEnum, GenderEnum


class User(Model):
    id = fields.IntField(pk=True, description="用户的唯一标识符")
    username = fields.CharField(max_length=100, description="用户的用户名")
    password = fields.CharField(max_length=100, description="用户的密码")
    email = fields.CharField(max_length=100, null=True, description="用户的邮箱地址")
    role = fields.IntEnumField(RoleEnum, description="用户角色: 0-学生, 1-教师, 2-管理员")
    gender = fields.IntEnumField(GenderEnum, description="用户性别: 0-女性, 1-男性, 2-保密")
    phone = fields.CharField(max_length=100, null=True, description="用户的联系电话")
    address = fields.CharField(max_length=100, null=True, description="用户的地址")
    desc = fields.TextField(description="用户的个人描述或介绍")
    avatar = fields.CharField(max_length=100, null=True, description="用户头像的URL")
    created_at = fields.DatetimeField(auto_now_add=True, description="用户创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="用户最后更新时间")

    class Meta:
        table = "user"

class Class(Model):
    id = fields.IntField(pk=True, description="班级的唯一标识符")
    class_name = fields.CharField(max_length=100, description="班级名称")
    teacher = fields.ForeignKeyField("models.User", related_name="classes", on_delete=fields.CASCADE, description="班级对应的教师")
    desc = fields.TextField(description="班级的详细描述")
    class_img = fields.CharField(max_length=100, null=True, description="班级图片的URL")
    created_at = fields.DatetimeField(auto_now_add=True, description="班级创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="班级最后更新时间")

    class Meta:
        table = "class"

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

class ClassAssignment(Model):
    id = fields.IntField(pk=True, description="班级作业关系的唯一标识符")
    class_ = fields.ForeignKeyField("models.Class", related_name="assignments", on_delete=fields.CASCADE, description="班级")
    assignment = fields.ForeignKeyField("models.Assignment", related_name="classes", on_delete=fields.CASCADE, description="作业")
    assigned_at = fields.DatetimeField(auto_now_add=True, description="作业分配时间")

    class Meta:
        table = "class_assignment"

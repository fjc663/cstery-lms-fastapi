from app.common.exceptions import ClassException
from app.models.baseModels.classBaseModel import ClassModel
from app.models.models import Class
from app.utils.classUtil import generate_class_code
from datetime import datetime
from tortoise.exceptions import DoesNotExist
from fastapi import status


# 创建班级
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
async def update_class(class_model: ClassModel):
    clas = class_model.model_dump(exclude_none=True)

    class_id = clas.pop('id')

    # 更新
    await Class.filter(id=class_id).update(**clas)


# 根据教师ID返回班级信息
async def get_class(teacher_id: int):
    return await Class.filter(teacher_id=teacher_id, is_deleted=False)


# 删除班级
async def delete_class(class_id: int):
    # 判断班级是否存在
    try:
        clas: Class = await Class.get(id=class_id)
    except DoesNotExist:
        raise ClassException(status_code=status.HTTP_404_NOT_FOUND, detail="班级不存在")

    # 判断是否已删除
    if clas.is_deleted:
        raise ClassException(status_code=status.HTTP_400_BAD_REQUEST, detail="班级已删除，请勿重复操作")

    # 逻辑删除
    await Class.filter(id=class_id).update(is_deleted=True)

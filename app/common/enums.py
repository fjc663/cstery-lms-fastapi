from enum import IntEnum

from tortoise.fields.base import StrEnum


# 性别枚举
class GenderEnum(IntEnum):
    FEMALE = 0
    MALE = 1
    OTHER = 2


# 作业格式提交枚举
class FormatEnum(StrEnum):
    TEXT = 'text'
    IMG = 'img'

# 图片类型
class ImageTypeEnum(IntEnum):
    CAROUSEL = 0
    PROMOTION = 1


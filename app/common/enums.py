from enum import Enum, IntEnum


class RoleEnum(IntEnum):
    STUDENT = 0
    TEACHER = 1
    ADMIN = 2

class GenderEnum(IntEnum):
    FEMALE = 0
    MALE = 1
    OTHER = 2
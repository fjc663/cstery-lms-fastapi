from fastapi import HTTPException

# 根异常
class TeacherBaseException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code

# 用户相关异常
class UserException(TeacherBaseException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(detail, status_code)

# 班级相关异常
class ClassException(TeacherBaseException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(detail, status_code)


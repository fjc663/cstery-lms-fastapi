from fastapi import HTTPException

# 根异常
class LmsBaseException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code

# 用户相关异常
class UserException(LmsBaseException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(detail, status_code)

# 班级相关异常
class ClassException(LmsBaseException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(detail, status_code)

# 作业相关异常
class TaskException(LmsBaseException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(detail, status_code)

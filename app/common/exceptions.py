from fastapi import HTTPException


# 用户相关异常
class UserException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code

# 班级相关异常
class ClassException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        self.detail = detail
        self.status_code = status_code


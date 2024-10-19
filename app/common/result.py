from typing import Optional, Any, List


# 统一返回结果
class Result:
    def __init__(self, code: int,  msg: Optional[str] = None, data: Optional[Any] = None):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def success(cls, data: Optional[Any] = None):
        return cls(code=1, data=data)

    @classmethod
    def error(cls, code: int = 0, msg: str = ''):
        return cls(code=code, msg=msg)

    def dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }


# 统一的分页查询结果
class PageResult:
    def __init__(self, total: int, records: List):
        self.total = total
        self.records = records

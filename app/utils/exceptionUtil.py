from fastapi import HTTPException

class UserDoesNotExistsException(HTTPException):
  def __init__(self, detail: str, status_code: int):
    self.detail = detail
    self.status_code = status_code
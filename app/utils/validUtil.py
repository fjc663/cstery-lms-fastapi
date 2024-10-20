# 校验用户名和密码只能是字母、数字和下划线
import re
from fastapi import status

from app.common.exceptions import UserException


def validate_username_password(username: str, password: str):
    # 正则表达式：\w+ 代表字母、数字、下划线
    if not re.match(r'^[0-9a-zA-Z_]{1,}$', username):
        raise UserException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名只能包含字母、数字和下划线")
    if not re.match(r'^[0-9a-zA-Z_]{1,}$', password):
        raise UserException(status_code=status.HTTP_400_BAD_REQUEST, detail="密码只能包含字母、数字和下划线")

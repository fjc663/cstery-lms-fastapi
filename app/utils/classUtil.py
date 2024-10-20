import hashlib
import time

# 生成班级邀请码
def generate_class_code(teacher_id):
    unique_string = f"{teacher_id}-{time.time()}"
    return hashlib.md5(unique_string.encode()).hexdigest()[:8]  # 取前8位作为班级编号

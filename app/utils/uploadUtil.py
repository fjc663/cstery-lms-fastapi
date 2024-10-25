import oss2
from app.config import ossConfig


def upload_file(file, filename):
    # 使用代码嵌入的访问密钥配置访问凭证。
    auth = oss2.Auth(ossConfig.access_key_id, ossConfig.access_key_secret)
    # 填写Bucket名称。
    bucket = oss2.Bucket(auth, ossConfig.endpoint, ossConfig.bucket_name)

    # 上传文件
    bucket.put_object(filename, file)

    # 文件访问路径
    path = f"https://{ossConfig.bucket_name}.{ossConfig.endpoint}/{filename}"

    return path

def delete_file(filename):
    # 使用代码嵌入的访问密钥配置访问凭证。
    auth = oss2.Auth(ossConfig.access_key_id, ossConfig.access_key_secret)
    # 填写Bucket名称。
    bucket = oss2.Bucket(auth, ossConfig.endpoint, ossConfig.bucket_name)

    # 删除文件
    bucket.delete_object(filename)


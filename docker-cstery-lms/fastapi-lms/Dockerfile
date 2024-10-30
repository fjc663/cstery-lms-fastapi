# 引入python版本
FROM python:3.9
 
# 设置时间
RUN ln -sf /usr/share/zoneinfo/Asia/Beijing/etc/localtime
 
# 输出时间
RUN echo 'Asia/Beijing' >/etc/timezone
 
# 设置工作目录
WORKDIR /cstery-lms
 
# 复制该文件到工作目录中，./requirements.txt表示当前目录下的requirements.txt文件。
COPY ./cstery-lms/requirements.txt /cstery-lms/requirements.txt
 
# 禁用缓存并批量安装包
RUN pip install --no-cache-dir --upgrade -r /cstery-lms/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
 
# 放开端口
EXPOSE 8080
 
# 命令行运行，启动uvicorn服务，指定ip和端口(--reload：让服务器在更新代码后重新启动。仅在开发时使用该选项。)
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
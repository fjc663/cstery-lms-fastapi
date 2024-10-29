## Cstery LearnHub学习管理系统

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-blue.svg)
![Tortoise-ORM](https://img.shields.io/badge/Tortoise--ORM-0.21.6-orange.svg)

一个基于FastApi、tortoise-orm的学习管理系统

功能包括：
- 创建班级
- 作业布置
- 批改作业
- 加入班级
- 完成作业
- 查看作业分数
- ....

### 运行该项目步骤：

- 在`/cstery-lms/app/settings.py`下配置连接数据库账号密码
- 在`/cstery-lms/app/config/ossConfig.py`配置文件存储的密钥（阿里云的OSS存储）
- 在连接的数据库下执行根目录下的的sql脚本
- pip install -r requirements.txt 下载所需库
- 运行app包下的main.py

> 默认端口是8080，对应的接口文档位置为 http://localhost:8080/docs

### 对应的前端项目

教师端：[https://github.com/fjc663/cstery-lms](https://github.com/fjc663/cstery-lms)
学生端：[https://github.com/fjc663/cstery-lms-stu](https://github.com/fjc663/cstery-lms-stu)



from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `student` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    `username` VARCHAR(100) NOT NULL  COMMENT '用户名',
    `password` VARCHAR(100) NOT NULL  COMMENT '密码',
    `name` VARCHAR(100) NOT NULL  COMMENT '姓名',
    `student_number` VARCHAR(100) NOT NULL  COMMENT '学号',
    `school` VARCHAR(100) NOT NULL  COMMENT '学校名称',
    `email` VARCHAR(100)   COMMENT '学生的邮箱地址',
    `gender` SMALLINT NOT NULL  COMMENT '用户性别: 0-女性, 1-男性, 2-保密',
    `phone` VARCHAR(100)   COMMENT '学生的联系电话',
    `address` VARCHAR(100)   COMMENT '学生的地址',
    `desc` LONGTEXT   COMMENT '学生的个人描述或介绍',
    `avatar` VARCHAR(100)   COMMENT '学生头像的URL',
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `teacher` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    `username` VARCHAR(100) NOT NULL  COMMENT '用户名',
    `password` VARCHAR(100) NOT NULL  COMMENT '密码',
    `name` VARCHAR(100) NOT NULL  COMMENT '姓名',
    `email` VARCHAR(100)   COMMENT '教师的邮箱地址',
    `gender` SMALLINT NOT NULL  COMMENT '用户性别: 0-女性, 1-男性, 2-保密',
    `phone` VARCHAR(100)   COMMENT '教师的联系电话',
    `address` VARCHAR(100)   COMMENT '教师的地址',
    `desc` LONGTEXT   COMMENT '教师的个人描述或介绍',
    `avatar` VARCHAR(100)   COMMENT '教师头像的URL',
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
        DROP TABLE IF EXISTS `user`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `student`;
        DROP TABLE IF EXISTS `teacher`;"""

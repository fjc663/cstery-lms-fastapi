from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student` MODIFY COLUMN `avatar` VARCHAR(255)   COMMENT '学生头像的URL';
        ALTER TABLE `student` MODIFY COLUMN `address` VARCHAR(255)   COMMENT '学生的地址';
        ALTER TABLE `student` MODIFY COLUMN `school` VARCHAR(255)   COMMENT '学校名称';
        ALTER TABLE `teacher` MODIFY COLUMN `avatar` VARCHAR(255)   COMMENT '教师头像的URL';
        ALTER TABLE `teacher` MODIFY COLUMN `address` VARCHAR(255)   COMMENT '教师的地址';
        ALTER TABLE `teacher` MODIFY COLUMN `phone` VARCHAR(30)   COMMENT '教师的联系电话';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student` MODIFY COLUMN `avatar` VARCHAR(100)   COMMENT '学生头像的URL';
        ALTER TABLE `student` MODIFY COLUMN `address` VARCHAR(100)   COMMENT '学生的地址';
        ALTER TABLE `student` MODIFY COLUMN `school` VARCHAR(100)   COMMENT '学校名称';
        ALTER TABLE `teacher` MODIFY COLUMN `avatar` VARCHAR(100)   COMMENT '教师头像的URL';
        ALTER TABLE `teacher` MODIFY COLUMN `address` VARCHAR(100)   COMMENT '教师的地址';
        ALTER TABLE `teacher` MODIFY COLUMN `phone` VARCHAR(100)   COMMENT '教师的联系电话';"""

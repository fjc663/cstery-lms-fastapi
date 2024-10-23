from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student` MODIFY COLUMN `school` VARCHAR(100)   COMMENT '学校名称';
        ALTER TABLE `student` MODIFY COLUMN `name` VARCHAR(100)   COMMENT '姓名';
        ALTER TABLE `student` MODIFY COLUMN `student_number` VARCHAR(100)   COMMENT '学号';
        ALTER TABLE `teacher` MODIFY COLUMN `name` VARCHAR(100)   COMMENT '姓名';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student` MODIFY COLUMN `school` VARCHAR(100) NOT NULL  COMMENT '学校名称';
        ALTER TABLE `student` MODIFY COLUMN `name` VARCHAR(100) NOT NULL  COMMENT '姓名';
        ALTER TABLE `student` MODIFY COLUMN `student_number` VARCHAR(100) NOT NULL  COMMENT '学号';
        ALTER TABLE `teacher` MODIFY COLUMN `name` VARCHAR(100) NOT NULL  COMMENT '姓名';"""

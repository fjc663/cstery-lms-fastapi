from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student` ADD `birthdate` DATE   COMMENT '出生日期';
        ALTER TABLE `student_assignment` DROP COLUMN `birthdate`;
        ALTER TABLE `teacher` ADD `birthdate` DATE   COMMENT '出生日期';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student` DROP COLUMN `birthdate`;
        ALTER TABLE `teacher` DROP COLUMN `birthdate`;
        ALTER TABLE `student_assignment` ADD `birthdate` DATE   COMMENT '出生日期';"""

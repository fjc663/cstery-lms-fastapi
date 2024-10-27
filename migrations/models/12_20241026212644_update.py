from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student_assignment` ADD `birthdate` DATE   COMMENT '出生日期';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student_assignment` DROP COLUMN `birthdate`;"""

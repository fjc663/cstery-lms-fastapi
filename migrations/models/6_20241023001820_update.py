from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `class` ADD `teacher_name` VARCHAR(100)   COMMENT '老师名称';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `class` DROP COLUMN `teacher_name`;"""

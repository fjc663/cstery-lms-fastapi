from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student_assignment` RENAME COLUMN `assigned_at` TO `created_at`;
        ALTER TABLE `student_assignment` ADD `updated_at` DATETIME(6) NOT NULL  COMMENT '更新提交作业时间';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student_assignment` RENAME COLUMN `created_at` TO `assigned_at`;
        ALTER TABLE `student_assignment` DROP COLUMN `updated_at`;"""

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `assignment` ADD `is_deleted` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `assignment` DROP COLUMN `is_deleted`;"""

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `class` MODIFY COLUMN `class_img` VARCHAR(255)   COMMENT '班级图片的URL';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `class` MODIFY COLUMN `class_img` VARCHAR(100)   COMMENT '班级图片的URL';"""

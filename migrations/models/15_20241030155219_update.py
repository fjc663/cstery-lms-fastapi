from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `home_image` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    `url` VARCHAR(255) NOT NULL  COMMENT '首页图片的url',
    `type` INT   COMMENT '图片的类型',
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  COMMENT '更新时间'
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `home_image`;"""

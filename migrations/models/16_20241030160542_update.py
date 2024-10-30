from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `home_image` ADD `is_stu` BOOL NOT NULL  COMMENT '是否是学生端的图片' DEFAULT 0;
        ALTER TABLE `home_image` ALTER COLUMN `type` SET DEFAULT 0;
        ALTER TABLE `home_image` MODIFY COLUMN `type` SMALLINT NOT NULL  COMMENT '图片的类型' DEFAULT 0;
        ALTER TABLE `home_image` MODIFY COLUMN `type` SMALLINT NOT NULL  COMMENT '图片的类型' DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `home_image` DROP COLUMN `is_stu`;
        ALTER TABLE `home_image` MODIFY COLUMN `type` INT   COMMENT '图片的类型';
        ALTER TABLE `home_image` MODIFY COLUMN `type` INT   COMMENT '图片的类型';
        ALTER TABLE `home_image` ALTER COLUMN `type` DROP DEFAULT;"""

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `assignment` MODIFY COLUMN `desc` LONGTEXT   COMMENT '作业的题目描述';
        ALTER TABLE `assignment` MODIFY COLUMN `images` JSON   COMMENT '作业题目图片的URL列表，以JSON格式存储';
        ALTER TABLE `student_assignment` ADD `desc` LONGTEXT   COMMENT '作业的解答描述';
        ALTER TABLE `student_assignment` ADD `title` VARCHAR(200) NOT NULL  COMMENT '作业解答标题';
        ALTER TABLE `student_assignment` ADD `images` JSON   COMMENT '作业解答图片的URL列表，以JSON格式存储';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `assignment` MODIFY COLUMN `desc` LONGTEXT   COMMENT '作业的详细描述';
        ALTER TABLE `assignment` MODIFY COLUMN `images` JSON   COMMENT '作业图片的URL列表，以JSON格式存储';
        ALTER TABLE `student_assignment` DROP COLUMN `desc`;
        ALTER TABLE `student_assignment` DROP COLUMN `title`;
        ALTER TABLE `student_assignment` DROP COLUMN `images`;"""

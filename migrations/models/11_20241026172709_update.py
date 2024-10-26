from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `assignment` MODIFY COLUMN `submission_format` VARCHAR(4)   COMMENT '作业提交的格式' DEFAULT 'text';
        ALTER TABLE `student` ALTER COLUMN `gender` SET DEFAULT 2;
        ALTER TABLE `student_assignment` ADD `score` INT   COMMENT '作业评分';
        ALTER TABLE `student_assignment` ADD `feedback` LONGTEXT   COMMENT '教师反馈';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `student` ALTER COLUMN `gender` DROP DEFAULT;
        ALTER TABLE `assignment` MODIFY COLUMN `submission_format` VARCHAR(50)   COMMENT '作业提交的格式' DEFAULT 'text';
        ALTER TABLE `student_assignment` DROP COLUMN `score`;
        ALTER TABLE `student_assignment` DROP COLUMN `feedback`;"""

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `assignment` ADD `clas_id` INT NOT NULL  COMMENT '班级';
        CREATE TABLE IF NOT EXISTS `student_assignment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    `assigned_at` DATETIME(6) NOT NULL  COMMENT '提交作业时间' DEFAULT CURRENT_TIMESTAMP(6),
    `assignment_id` INT NOT NULL COMMENT '作业',
    `student_id` INT NOT NULL COMMENT '学生',
    CONSTRAINT `fk_student__assignme_3f850ded` FOREIGN KEY (`assignment_id`) REFERENCES `assignment` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_student__student_0cb95d16` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        DROP TABLE IF EXISTS `class_assignment`;
        ALTER TABLE `assignment` ADD CONSTRAINT `fk_assignme_class_91a2c5c9` FOREIGN KEY (`clas_id`) REFERENCES `class` (`id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `assignment` DROP FOREIGN KEY `fk_assignme_class_91a2c5c9`;
        ALTER TABLE `assignment` DROP COLUMN `clas_id`;
        DROP TABLE IF EXISTS `student_assignment`;"""

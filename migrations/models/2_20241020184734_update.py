from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `class_assignment` DROP FOREIGN KEY `fk_class_as_class_5fc661fa`;
        ALTER TABLE `class_assignment` RENAME COLUMN `class__id` TO `clas_id`;
        CREATE TABLE IF NOT EXISTS `class_student` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '班级学生关系的唯一标识符',
    `created_at` DATETIME(6) NOT NULL  COMMENT '学生加入时间' DEFAULT CURRENT_TIMESTAMP(6),
    `clas_id` INT NOT NULL COMMENT '班级',
    `student_id` INT NOT NULL COMMENT '学生',
    CONSTRAINT `fk_class_st_class_8df71cb2` FOREIGN KEY (`clas_id`) REFERENCES `class` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_class_st_user_697cdd34` FOREIGN KEY (`student_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        ALTER TABLE `class_assignment` ADD CONSTRAINT `fk_class_as_class_08b8b225` FOREIGN KEY (`clas_id`) REFERENCES `class` (`id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `class_assignment` DROP FOREIGN KEY `fk_class_as_class_08b8b225`;
        ALTER TABLE `class_assignment` RENAME COLUMN `clas_id` TO `class__id`;
        DROP TABLE IF EXISTS `class_student`;
        ALTER TABLE `class_assignment` ADD CONSTRAINT `fk_class_as_class_5fc661fa` FOREIGN KEY (`class__id`) REFERENCES `class` (`id`) ON DELETE CASCADE;"""

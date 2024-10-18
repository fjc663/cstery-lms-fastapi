from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `assignment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(200) NOT NULL,
    `desc` LONGTEXT,
    `due_date` DATE,
    `allow_late_submission` BOOL NOT NULL  DEFAULT 0,
    `submission_format` VARCHAR(50)   DEFAULT 'text',
    `images` JSON,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(100) NOT NULL,
    `password` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100),
    `role` INT NOT NULL,
    `gender` INT NOT NULL,
    `phone` VARCHAR(100),
    `address` VARCHAR(100),
    `desc` LONGTEXT NOT NULL,
    `avatar` VARCHAR(100),
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `class` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `class_name` VARCHAR(100) NOT NULL,
    `desc` LONGTEXT NOT NULL,
    `class_img` VARCHAR(100),
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `teacher_id` INT NOT NULL,
    CONSTRAINT `fk_class_user_bcaf4a5a` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `class_assignment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `assigned_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `assignment_id` INT NOT NULL,
    `class__id` INT NOT NULL,
    CONSTRAINT `fk_class_as_assignme_73229068` FOREIGN KEY (`assignment_id`) REFERENCES `assignment` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_class_as_class_5fc661fa` FOREIGN KEY (`class__id`) REFERENCES `class` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

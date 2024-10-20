from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `assignment` MODIFY COLUMN `due_date` DATE   COMMENT '作业截止日期';
        ALTER TABLE `assignment` MODIFY COLUMN `desc` LONGTEXT   COMMENT '作业的详细描述';
        ALTER TABLE `assignment` MODIFY COLUMN `submission_format` VARCHAR(50)   COMMENT '作业提交的格式' DEFAULT 'text';
        ALTER TABLE `assignment` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL  COMMENT '作业创建时间' DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `assignment` MODIFY COLUMN `allow_late_submission` BOOL NOT NULL  COMMENT '是否允许截止后提交作业' DEFAULT 0;
        ALTER TABLE `assignment` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL  COMMENT '作业最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `assignment` MODIFY COLUMN `title` VARCHAR(200) NOT NULL  COMMENT '作业标题';
        ALTER TABLE `assignment` MODIFY COLUMN `images` JSON   COMMENT '作业图片的URL列表，以JSON格式存储';
        ALTER TABLE `class` ADD `is_deleted` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0;
        ALTER TABLE `class` ADD `class_code` VARCHAR(20) NOT NULL UNIQUE COMMENT '班级邀请码';
        ALTER TABLE `class` MODIFY COLUMN `desc` LONGTEXT   COMMENT '班级的详细描述';
        ALTER TABLE `class` MODIFY COLUMN `desc` LONGTEXT   COMMENT '班级的详细描述';
        ALTER TABLE `class` MODIFY COLUMN `teacher_id` INT NOT NULL  COMMENT '班级对应的教师';
        ALTER TABLE `class` MODIFY COLUMN `class_img` VARCHAR(100)   COMMENT '班级图片的URL';
        ALTER TABLE `class` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL  COMMENT '班级创建时间' DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `class` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL  COMMENT '班级最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `class` MODIFY COLUMN `class_name` VARCHAR(100) NOT NULL  COMMENT '班级名称';
        ALTER TABLE `class_assignment` MODIFY COLUMN `assigned_at` DATETIME(6) NOT NULL  COMMENT '作业分配时间' DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `class_assignment` MODIFY COLUMN `class__id` INT NOT NULL  COMMENT '班级';
        ALTER TABLE `class_assignment` MODIFY COLUMN `assignment_id` INT NOT NULL  COMMENT '作业';
        ALTER TABLE `user` MODIFY COLUMN `password` VARCHAR(100) NOT NULL  COMMENT '用户的密码';
        ALTER TABLE `user` MODIFY COLUMN `desc` LONGTEXT   COMMENT '用户的个人描述或介绍';
        ALTER TABLE `user` MODIFY COLUMN `desc` LONGTEXT   COMMENT '用户的个人描述或介绍';
        ALTER TABLE `user` MODIFY COLUMN `avatar` VARCHAR(100)   COMMENT '用户头像的URL';
        ALTER TABLE `user` MODIFY COLUMN `address` VARCHAR(100)   COMMENT '用户的地址';
        ALTER TABLE `user` MODIFY COLUMN `role` SMALLINT NOT NULL  COMMENT '用户角色: 0-学生, 1-教师, 2-管理员';
        ALTER TABLE `user` MODIFY COLUMN `username` VARCHAR(100) NOT NULL  COMMENT '用户的用户名';
        ALTER TABLE `user` MODIFY COLUMN `phone` VARCHAR(100)   COMMENT '用户的联系电话';
        ALTER TABLE `user` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL  COMMENT '用户创建时间' DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` MODIFY COLUMN `gender` SMALLINT NOT NULL  COMMENT '用户性别: 0-女性, 1-男性, 2-保密';
        ALTER TABLE `user` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL  COMMENT '用户最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL  COMMENT '用户最后更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(100)   COMMENT '用户的邮箱地址';
        ALTER TABLE `class` ADD UNIQUE INDEX `uid_class_class_c_02afb4` (`class_code`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `class` DROP INDEX `idx_class_class_c_02afb4`;
        ALTER TABLE `user` MODIFY COLUMN `password` VARCHAR(100) NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `desc` LONGTEXT NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `desc` LONGTEXT NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `avatar` VARCHAR(100);
        ALTER TABLE `user` MODIFY COLUMN `address` VARCHAR(100);
        ALTER TABLE `user` MODIFY COLUMN `role` INT NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `username` VARCHAR(100) NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `phone` VARCHAR(100);
        ALTER TABLE `user` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` MODIFY COLUMN `gender` INT NOT NULL;
        ALTER TABLE `user` MODIFY COLUMN `updated_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` MODIFY COLUMN `updated_at` DATETIME(6)   DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` MODIFY COLUMN `email` VARCHAR(100);
        ALTER TABLE `class` DROP COLUMN `is_deleted`;
        ALTER TABLE `class` DROP COLUMN `class_code`;
        ALTER TABLE `class` MODIFY COLUMN `desc` LONGTEXT NOT NULL;
        ALTER TABLE `class` MODIFY COLUMN `desc` LONGTEXT NOT NULL;
        ALTER TABLE `class` MODIFY COLUMN `teacher_id` INT NOT NULL;
        ALTER TABLE `class` MODIFY COLUMN `class_img` VARCHAR(100);
        ALTER TABLE `class` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `class` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `class` MODIFY COLUMN `class_name` VARCHAR(100) NOT NULL;
        ALTER TABLE `assignment` MODIFY COLUMN `due_date` DATE;
        ALTER TABLE `assignment` MODIFY COLUMN `desc` LONGTEXT;
        ALTER TABLE `assignment` MODIFY COLUMN `submission_format` VARCHAR(50)   DEFAULT 'text';
        ALTER TABLE `assignment` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `assignment` MODIFY COLUMN `allow_late_submission` BOOL NOT NULL  DEFAULT 0;
        ALTER TABLE `assignment` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `assignment` MODIFY COLUMN `title` VARCHAR(200) NOT NULL;
        ALTER TABLE `assignment` MODIFY COLUMN `images` JSON;
        ALTER TABLE `class_assignment` MODIFY COLUMN `assigned_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `class_assignment` MODIFY COLUMN `class__id` INT NOT NULL;
        ALTER TABLE `class_assignment` MODIFY COLUMN `assignment_id` INT NOT NULL;"""

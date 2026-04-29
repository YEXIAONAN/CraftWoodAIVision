-- ============================================================
-- CraftWoodAIVision · 匠木云检
-- MySQL Database Initialization Script
-- ============================================================

CREATE DATABASE IF NOT EXISTS craftwood
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE craftwood;

-- ---- Users ----
CREATE TABLE IF NOT EXISTS `user` (
  `id`            INT           NOT NULL AUTO_INCREMENT,
  `username`      VARCHAR(64)   NOT NULL,
  `hashed_password` VARCHAR(256) NOT NULL,
  `name`          VARCHAR(64)   NOT NULL,
  `role`          VARCHAR(32)   NOT NULL DEFAULT 'admin' COMMENT 'admin, inspector, sales, consumer',
  `avatar`        VARCHAR(256)  NOT NULL DEFAULT '',
  `is_active`     TINYINT(1)    NOT NULL DEFAULT 1,
  `created_at`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `ix_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ---- Products ----
CREATE TABLE IF NOT EXISTS `product` (
  `id`            VARCHAR(32)   NOT NULL,
  `name`          VARCHAR(128)  NOT NULL,
  `type`          VARCHAR(64)   NOT NULL DEFAULT '红木家具',
  `dimensions`    VARCHAR(128)  NOT NULL DEFAULT '',
  `material`      VARCHAR(64)   NOT NULL DEFAULT '',
  `batch`         VARCHAR(64)   NOT NULL DEFAULT '',
  `status`        VARCHAR(32)   NOT NULL DEFAULT '已入库' COMMENT '已入库, 仓储中, 待出库, 已出库, 已归档',
  `grade`         VARCHAR(16)   NOT NULL DEFAULT 'A级',
  `inspector`     VARCHAR(64)   NOT NULL DEFAULT '',
  `image`         VARCHAR(256)  NOT NULL DEFAULT '',
  `date`          VARCHAR(32)   NOT NULL DEFAULT '',
  `created_at`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ---- Inspection Records ----
CREATE TABLE IF NOT EXISTS `inspection_record` (
  `id`              VARCHAR(32)   NOT NULL,
  `product_id`      VARCHAR(32)   NOT NULL,
  `product_name`    VARCHAR(128)  NOT NULL DEFAULT '',
  `date`            VARCHAR(32)   NOT NULL DEFAULT '',
  `inspector`       VARCHAR(64)   NOT NULL DEFAULT '',
  `scene`           VARCHAR(32)   NOT NULL DEFAULT '入库检测' COMMENT '入库检测, 仓储巡检, 出库复检',
  `risk`            VARCHAR(16)   NOT NULL DEFAULT 'low' COMMENT 'low, medium, high',
  `risk_label`      VARCHAR(16)   NOT NULL DEFAULT '低风险',
  `score`           FLOAT         NOT NULL DEFAULT 0,
  `defects`         JSON          NULL,
  `image`           VARCHAR(256)  NOT NULL DEFAULT '',
  `annotated_image` VARCHAR(256)  NOT NULL DEFAULT '',
  `notes`           TEXT          NULL,
  `reviewed`        TINYINT(1)    NOT NULL DEFAULT 0,
  `created_at`      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_inspection_product_id` (`product_id`),
  CONSTRAINT `fk_inspection_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ---- Warehouse Records ----
CREATE TABLE IF NOT EXISTS `warehouse_record` (
  `id`            VARCHAR(32)   NOT NULL,
  `product_id`    VARCHAR(32)   NOT NULL,
  `product_name`  VARCHAR(128)  NOT NULL DEFAULT '',
  `action`        VARCHAR(32)   NOT NULL COMMENT '入库, 仓储巡检, 出库复检, 出库',
  `operator`      VARCHAR(64)   NOT NULL DEFAULT '',
  `date`          VARCHAR(32)   NOT NULL DEFAULT '',
  `notes`         TEXT          NULL,
  `status`        VARCHAR(32)   NOT NULL DEFAULT '已完成' COMMENT '已完成, 待处理',
  `created_at`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_warehouse_product_id` (`product_id`),
  CONSTRAINT `fk_warehouse_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ---- Report Records ----
CREATE TABLE IF NOT EXISTS `report_record` (
  `id`            VARCHAR(32)   NOT NULL,
  `product_id`    VARCHAR(32)   NOT NULL,
  `product_name`  VARCHAR(128)  NOT NULL DEFAULT '',
  `date`          VARCHAR(32)   NOT NULL DEFAULT '',
  `inspector`     VARCHAR(64)   NOT NULL DEFAULT '',
  `conclusion`    VARCHAR(32)   NOT NULL DEFAULT '合格' COMMENT '合格, 条件合格, 需复检',
  `risk`          VARCHAR(16)   NOT NULL DEFAULT '低风险',
  `score`         FLOAT         NOT NULL DEFAULT 0,
  `file_path`     VARCHAR(256)  NOT NULL DEFAULT '',
  `created_at`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_report_product_id` (`product_id`),
  CONSTRAINT `fk_report_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ---- After-Sales Records ----
CREATE TABLE IF NOT EXISTS `after_sales_record` (
  `id`            VARCHAR(32)   NOT NULL,
  `product_id`    VARCHAR(32)   NOT NULL,
  `product_name`  VARCHAR(128)  NOT NULL DEFAULT '',
  `type`          VARCHAR(32)   NOT NULL COMMENT '运输损坏, 质量异议, 表面瑕疵, 尺寸不符',
  `description`   TEXT          NULL,
  `status`        VARCHAR(32)   NOT NULL DEFAULT '待处理' COMMENT '待处理, 处理中, 已完成, 已关闭',
  `customer`      VARCHAR(64)   NOT NULL DEFAULT '',
  `date`          VARCHAR(32)   NOT NULL DEFAULT '',
  `handler`       VARCHAR(64)   NOT NULL DEFAULT '',
  `created_at`    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `ix_aftersales_product_id` (`product_id`),
  CONSTRAINT `fk_aftersales_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ---- Trace Records (access logs) ----
CREATE TABLE IF NOT EXISTS `trace_record` (
  `id`              INT           NOT NULL AUTO_INCREMENT,
  `product_id`      VARCHAR(32)   NOT NULL,
  `access_time`     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `access_source`   VARCHAR(64)   NOT NULL DEFAULT '',
  `access_content`  VARCHAR(256)  NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  INDEX `ix_trace_product_id` (`product_id`),
  CONSTRAINT `fk_trace_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

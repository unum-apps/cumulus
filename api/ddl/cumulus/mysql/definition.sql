CREATE TABLE IF NOT EXISTS `cumulus`.`bucket` (
  `id` VARCHAR(255) COLLATE utf8mb4_bin NOT NULL,
  `version` BIGINT NOT NULL DEFAULT 1,
  `unum` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255),
  `what` JSON NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `cumulus`.`entity` (
  `id` VARCHAR(255) COLLATE utf8mb4_bin NOT NULL,
  `version` BIGINT NOT NULL DEFAULT 1,
  `unum` VARCHAR(255) NOT NULL,
  `who` VARCHAR(255),
  `unifist_unum` VARCHAR(255) NOT NULL DEFAULT 'unifist',
  `what` JSON NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `cumulus`.`flush` (
  `id` VARCHAR(255) COLLATE utf8mb4_bin NOT NULL,
  `version` BIGINT NOT NULL DEFAULT 1,
  `unum` VARCHAR(255) NOT NULL,
  `entity_id` VARCHAR(255),
  `when` BIGINT NOT NULL,
  `what` JSON NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `when` (`when`)
);

CREATE TABLE IF NOT EXISTS `cumulus`.`scat` (
  `id` VARCHAR(255) COLLATE utf8mb4_bin NOT NULL,
  `version` BIGINT NOT NULL DEFAULT 1,
  `unum` VARCHAR(255) NOT NULL,
  `entity_id` VARCHAR(255),
  `description` VARCHAR(255),
  `when` BIGINT NOT NULL,
  `what` JSON NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `when` (`when`)
);

CREATE TABLE IF NOT EXISTS `cumulus`.`unifist` (
  `id` VARCHAR(255) COLLATE utf8mb4_bin NOT NULL,
  `version` BIGINT NOT NULL DEFAULT 1,
  `unum` VARCHAR(255) NOT NULL,
  `who` VARCHAR(255),
  `what` JSON NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `cumulus`.`unifist_unum` (
  `id` VARCHAR(255) COLLATE utf8mb4_bin NOT NULL,
  `unifist_id` VARCHAR(255),
  `unum_id` VARCHAR(255),
  `version` BIGINT NOT NULL DEFAULT 1,
  `unum` VARCHAR(255) NOT NULL,
  `what` JSON NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE `unifist_id_unum_id` (`unifist_id`,`unum_id`)
);

CREATE TABLE IF NOT EXISTS `cumulus`.`unum` (
  `id` VARCHAR(255) COLLATE utf8mb4_bin NOT NULL,
  `version` BIGINT NOT NULL DEFAULT 1,
  `unum` VARCHAR(255) NOT NULL,
  `who` VARCHAR(255),
  `what` JSON NOT NULL,
  PRIMARY KEY (`id`)
);

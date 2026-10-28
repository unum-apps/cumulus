ALTER TABLE `cumulus`.`bucket`
  CHANGE `unum` `home` VARCHAR(255) NOT NULL;

ALTER TABLE `cumulus`.`entity`
  CHANGE `unum` `home` VARCHAR(255) NOT NULL;

ALTER TABLE `cumulus`.`flush`
  CHANGE `unum` `home` VARCHAR(255) NOT NULL;

ALTER TABLE `cumulus`.`scat`
  CHANGE `unum` `home` VARCHAR(255) NOT NULL;

ALTER TABLE `cumulus`.`unifist`
  CHANGE `unum` `home` VARCHAR(255) NOT NULL;

ALTER TABLE `cumulus`.`unifist_unum`
  CHANGE `unum` `home` VARCHAR(255) NOT NULL;

ALTER TABLE `cumulus`.`unum`
  CHANGE `unum` `home` VARCHAR(255) NOT NULL;

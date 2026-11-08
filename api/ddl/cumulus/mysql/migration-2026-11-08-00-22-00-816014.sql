ALTER TABLE `cumulus`.`bucket`
  ADD `entity_id` VARCHAR(255),
  ADD `criterion` JSON NOT NULL;

;

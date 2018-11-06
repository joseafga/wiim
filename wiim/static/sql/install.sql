CREATE TABLE `server` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `uid` VARCHAR(64) NOT NULL
)
CHARACTER SET 'utf8' 
COLLATE 'utf8_unicode_ci';

CREATE TABLE `site` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(64) NOT NULL,
  `comment` VARCHAR(120) NOT NULL
)
CHARACTER SET 'utf8' 
COLLATE 'utf8_unicode_ci';

CREATE TABLE `tag` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `server` INTEGER NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `alias` VARCHAR(120) NOT NULL,
  `unit` VARCHAR(64) NOT NULL,
  `comment` VARCHAR(120) NOT NULL
  `icon` VARCHAR(255) NOT NULL
)
CHARACTER SET 'utf8' 
COLLATE 'utf8_unicode_ci';

CREATE INDEX `idx_tag__server` ON `tag` (`server`);

ALTER TABLE `tag` ADD CONSTRAINT `fk_tag__server` FOREIGN KEY (`server`) REFERENCES `server` (`id`);

CREATE TABLE `record` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `tag` INTEGER NOT NULL,
  `time_opc` DATETIME(3),
  `time_db` TIMESTAMP(3),
  `value` VARCHAR(120) NOT NULL,
  `quality` VARCHAR(64) NOT NULL
) engine = MyISAM 
CHARACTER SET 'utf8' 
COLLATE 'utf8_unicode_ci';

CREATE INDEX `idx_record__tag` ON `record` (`tag`);

ALTER TABLE `record` ADD CONSTRAINT `fk_record__tag` FOREIGN KEY (`tag`) REFERENCES `tag` (`id`);

CREATE TABLE `zone` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `site` INTEGER NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `comment` VARCHAR(120) NOT NULL
)
CHARACTER SET 'utf8' 
COLLATE 'utf8_unicode_ci';

CREATE INDEX `idx_zone__site` ON `zone` (`site`);

ALTER TABLE `zone` ADD CONSTRAINT `fk_zone__site` FOREIGN KEY (`site`) REFERENCES `site` (`id`);

CREATE TABLE `process` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `zone` INTEGER NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `comment` VARCHAR(120) NOT NULL
)
CHARACTER SET 'utf8' 
COLLATE 'utf8_unicode_ci';

CREATE INDEX `idx_process__zone` ON `process` (`zone`);

ALTER TABLE `process` ADD CONSTRAINT `fk_process__zone` FOREIGN KEY (`zone`) REFERENCES `zone` (`id`);

CREATE TABLE `process_tags` (
  `tag` INTEGER NOT NULL,
  `process` INTEGER NOT NULL,
  CONSTRAINT `pk_process_tags` PRIMARY KEY (`tag`, `process`)
)
CHARACTER SET 'utf8' 
COLLATE 'utf8_unicode_ci';

CREATE INDEX `idx_process_tags` ON `process_tags` (`process`);

ALTER TABLE `process_tags` ADD CONSTRAINT `fk_process_tags__process` FOREIGN KEY (`process`) REFERENCES `process` (`id`);

ALTER TABLE `process_tags` ADD CONSTRAINT `fk_process_tags__tag` FOREIGN KEY (`tag`) REFERENCES `tag` (`id`)
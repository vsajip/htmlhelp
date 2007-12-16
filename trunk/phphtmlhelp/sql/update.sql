-- Version 1.0 => 1.1 --

CREATE TABLE IF NOT EXISTS `lexeme_page` (
  `book_id` smallint(5) unsigned NOT NULL default '0',
  `lexeme` varchar(31) binary NOT NULL default '',
  `pages` blob NOT NULL,
  KEY `lexeme` (`book_id`, `lexeme`(6))
) TYPE=MyISAM;

DROP TABLE IF EXISTS `lexeme`;
DROP TABLE IF EXISTS `lexeme_link`;

UPDATE `version` 
SET `minor`=1 
WHERE `major`=1 AND `minor`=0;


-- Version 1.1 => 1.2 --

ALTER TABLE `metadata` 
DROP PRIMARY KEY ,
ADD PRIMARY KEY ( `book_id` , `name` );

ALTER TABLE `metadata` 
DROP INDEX `name`,
ADD INDEX `name` (`name`, `value`(5));

DELETE
FROM book_alias
WHERE alias = book_id;

DELETE
FROM `book_tag`
WHERE book_name IS NOT NULL;

ALTER TABLE `book_tag` 
DROP INDEX `book_name`;

ALTER TABLE `book_tag` 
CHANGE `book_name` `book_id` SMALLINT(5) UNSIGNED NOT NULL;

ALTER TABLE `book_tag` 
DROP INDEX `tag_id` ,
ADD PRIMARY KEY ( `tag_id` , `book_id` );

UPDATE `version` 
SET `minor`=2 
WHERE `major`=1 AND `minor`=1;


-- Version 1.2 => 1.3 --

ALTER TABLE `book` DROP INDEX `title`;

CREATE TABLE `alias` (
  `id` smallint(5) unsigned NOT NULL auto_increment,
  `alias` varchar(31) NOT NULL default '',
  `book_id` smallint(5) unsigned NOT NULL default '0',
  PRIMARY KEY  (`id`),
  UNIQUE KEY `alias` (`alias`),
  UNIQUE KEY `book_id` (`book_id`)
) TYPE=MyISAM;

INSERT IGNORE
INTO alias (alias, book_id)
SELECT value, book_id
FROM metadata
WHERE name = 'name';

DROP TABLE book_alias;

CREATE TABLE alias_tag (
  alias_id smallint(5) unsigned NOT NULL default '0',
  tag_id smallint(5) unsigned NOT NULL default '0',
  PRIMARY KEY  (tag_id,alias_id)
) TYPE=MyISAM;

INSERT IGNORE
INTO alias_tag (tag_id, alias_id)
SELECT tag_id, alias.id
FROM book_tag
	INNER JOIN alias USING(book_id);
	
DROP TABLE book_tag;

UPDATE `version` 
SET `minor`=3 
WHERE `major`=1 AND `minor`=2;


-- Version 1.3 => 1.4 --

ALTER TABLE `alias` ADD `book_hits` INT UNSIGNED DEFAULT '0' NOT NULL ,
ADD `page_hits` INT UNSIGNED DEFAULT '0' NOT NULL ;

UPDATE `version` 
SET `minor`=4 
WHERE `major`=1 AND `minor`=3;

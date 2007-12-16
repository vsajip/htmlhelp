SELECT
	IFNULL(alias, "") AS name,
	IFNULL(GROUP_CONCAT(DISTINCT tag ORDER BY tag ASC SEPARATOR ","), "") AS tags
FROM tag 
	RIGHT JOIN alias_tag ON tag_id = tag.id
	RIGHT JOIN alias ON alias.id = alias_id
GROUP BY alias
ORDER BY alias

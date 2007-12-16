#!/usr/bin/env python

import sys

sys.stdout.write(
"""CREATE TEMPORARY TABLE temp_alias_tag (
  alias varchar(31) NOT NULL,
  tag varchar(31) NOT NULL
);
""")

sys.stdout.write(
"""INSERT
INTO temp_alias_tag (alias, tag)
VALUES """)
sep = ''
for line in sys.stdin:
	line = line[:-1]
	alias, tags = line.split('\t')
	tags = [tag.strip() for tag in tags.split(',')]

	if alias:
		for tag in tags:
			if tag:
				sys.stdout.write(sep)
				sys.stdout.write('("%s", "%s")' % (alias, tag))
				sep = ',\n\t'
sys.stdout.write(""";

""")


sys.stdout.write(
"""INSERT IGNORE
INTO tag (tag)
SELECT tag
FROM temp_alias_tag;

""")
sys.stdout.write(
"""INSERT IGNORE
INTO alias (alias)
SELECT alias
FROM temp_alias_tag;

""")
sys.stdout.write(
"""INSERT IGNORE
INTO alias_tag (tag_id, alias_id)
SELECT tag.id, alias.id
FROM tag
LEFT JOIN temp_alias_tag USING(tag)
LEFT JOIN alias USING(alias);

""")
sys.stdout.write(
"""DROP /*!40000 TEMPORARY */ TABLE temp_alias_tag;

""")

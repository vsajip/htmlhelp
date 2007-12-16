# Makefile


# Variables

DATABASE = htmlhelp
USERNAME = htmlhelp
# TODO: deal with passwords (securely?)

MYSQL = mysql
MYSQL_FLAGS = \
	--user=$(USERNAME)

MYSQLDUMP = mysqldump
MYSQLDUMP_FLAGS = \
	$(MYSQL_FLAGS) \
	--skip-lock-tables \
	--compatible=mysql323 \
	--complete-insert


# Default targets

default: $(patsubst %.txt,%.sql,$(wildcard *.txt))

.PHONY: default


# Export database

export: \
	export-create.sql export-tags.txt export-book_tags.txt

export-structure.sql: MYSQLDUMP_FLAGS += --add-drop-table --no-data

export-version.sql: MYSQLDUMP_FLAGS += --skip-comments --no-create-info --complete-insert --skip-add-locks
export-version.sql: TABLES = version

export-tags.sql: MYSQLDUMP_FLAGS += --skip-comments --no-create-info --complete-insert --skip-add-locks
export-tags.sql: TABLES = tag alias_tag alias

export-create.sql: export-structure.sql export-version.sql
	cat $(patsubst export-%,%,$^) > $(patsubst export-%,%,$@)
	rm -f $(patsubst export-%,%,$^)

export-%.txt: export_%.sql
	$(MYSQL) $(MYSQL_FLAGS) --skip-column-names --table=false $(DATABASE) < $< > $*.txt

export-%.sql:
	$(MYSQLDUMP) \
		$(MYSQLDUMP_FLAGS) \
		$(DATABASE) $(TABLES) \
	| sed -e '/^\/\*!.*\*\/;$$/d' > $*.sql

.PHONY: export export-%


# Import initial database

import: \
	import-create.sql \
	import-tags.sql \
	import-book_tags.sql

import-%: %
	$(MYSQL) $(MYSQL_FLAGS) $(DATABASE) < $<

.PHONY: import import-%


# Implicit rules

%.sql: %.sed %.txt
	sed -f $^ > $@

%.sql: %.py %.txt
	python $*.py < $*.txt > $@



# Clean

clean:
	-rm -f $(wildcard *.sql)

.PHONY: clean


<?php

require_once 'inc/config.inc.php';
require_once 'lib/book_catalog.lib.php';

// get this lexeme number
$result = mysql_query(
	"SELECT lexeme, LENGTH(pages)/3 AS count
	FROM lexeme_page
	ORDER BY count DESC, lexeme ASC"
) or die(mysql_error());
while(list($lexeme, $count) = mysql_fetch_row($result))
	printf("%-32s %5d\n", $lexeme, $count);
?>

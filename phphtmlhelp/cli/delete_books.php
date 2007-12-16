<?php

if(php_sapi_name() != 'cli')
	die("You're not using CLI PHP");

require_once 'inc/config.inc.php';
require_once 'lib/book_catalog.lib.php';

/*
$catalog = new BookCatalog();
$books = $catalog->enumerate_book_ids();
foreach($books as $book_id => $book_title)
{
	echo "Deleting '$book_title'...\n";
	$book = $catalog->get_book_by_id($book_id);
	$book->delete();
}
*/

$tables = array(
	"book",
	"metadata",
	"toc_entry",
	"index_entry",
	"index_link",
	"page",
	"lexeme_page",
);

foreach($tables as $table)
	mysql_query("TRUNCATE $table");

?>

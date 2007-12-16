<?php

if(php_sapi_name() != 'cli')
	die("You're not using CLI PHP");

require_once 'inc/config.inc.php';
require_once 'lib/book_catalog.lib.php';

$catalog = new BookCatalog();
$books = $catalog->enumerate_book_ids();
foreach($books as $book_id => $book_title)
{
	echo "Indexing '$book_title'...";
	$start_time = time();

	$book = $catalog->get_book_by_id($book_id);
	$book->index_fulltext();
	
	$finish_time = time();
	$ellapsed_time = $finish_time - $start_time;
	echo " ($ellapsed_time sec)\n";
}

?>

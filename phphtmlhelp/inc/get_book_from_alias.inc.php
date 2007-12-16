<?php

require_once 'lib/book_catalog.lib.php';

$catalog = new BookCatalog();
$book = $catalog->get_book_from_alias($alias);
if(!isset($book))
{
	header("Status: 404 Not Found");
	
	echo '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">';
	echo '<html><head>';
	echo '<title>404 Not Found</title>';
	echo '</head><body>';
	echo '<h1>Not Found</h1>';
	echo '<p>The requested book was not found.</p>';
	echo '</body></html>';
	
	exit;
}

?>

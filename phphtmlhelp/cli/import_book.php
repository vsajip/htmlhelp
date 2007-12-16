<?php

if(php_sapi_name() != 'cli')
	die("You're not using CLI PHP");

require_once 'inc/config.inc.php';
require_once 'lib/book_catalog.lib.php';

$catalog = new BookCatalog();
for($i = 1; $i < $argc; ++$i)
{
	$filename = $argv[$i];

	echo "Importing '$filename'...";
	$start_time = time();

	$catalog->import_book($filename);
	
	$finish_time = time();
	$ellapsed_time = $finish_time - $start_time;
	echo " ($ellapsed_time sec)\n";
}

?>

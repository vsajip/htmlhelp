<?php
	require_once 'inc/config.inc.php';

	$alias = $_GET['book'];
	require 'inc/get_book_from_alias.inc.php';
	
	# Enable HTTP compression
	ob_start("ob_gzhandler");
	
	header('Content-type: application/vnd.mozilla.xul+xml');

	echo '<?xml version="1.0" encoding="' . $internal_encoding . '"?>';
	echo '<?xml-stylesheet href="chrome://global/skin/" type="text/css"?>';

	echo '<window xmlns="http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul">';

	echo '<script src="js/searchfrm.js"/>';

	$query = $_GET['query'];	
	
	echo '<textbox id="query" type="autocomplete" value="' . htmlspecialchars($query, ENT_QUOTES) . '" onkeypress="onQueryKeypress(event, \'' . htmlspecialchars($alias, ENT_QUOTES) . '\');"/>';

	echo '<listbox seltype="single" flex="1" onselect="onSearchSelect(event, \'' . htmlspecialchars($alias, ENT_QUOTES) . '\');">';
	if($query)
	{
		$entries = $book->search($query);
		foreach($entries as $entry)
		{
			list($title, $path) = $entry;
			echo '<listitem label="' . htmlspecialchars($title, ENT_QUOTES) . '" value="' . $path .'"/>';
		}
	}
	echo '</listbox>';

	echo '</window>';
?>

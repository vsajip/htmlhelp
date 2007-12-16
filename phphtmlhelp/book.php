<?php
	require_once 'inc/config.inc.php';

	$alias = $_GET['book'];
	require 'inc/get_book_from_alias.inc.php'; 

	$catalog->book_hit($alias);

	header('Content-Type: text/html; charset=' . $internal_encoding);
		
	echo '<?xml version="1.0" encoding="' . $internal_encoding . '"?>';
	echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">';
	
	echo '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">';
	echo '<head>';
	echo '<meta http-equiv="Content-Type" content="text/html; charset=' . $internal_encoding . '"/>';
	echo '<title>' . htmlspecialchars($book->title(), ENT_NOQUOTES) . '</title>';
	echo '<link href="css/html.css" type="text/css" rel="stylesheet"/>';
	echo '</head>';

	// Unless the 'noxul' param is given then embed a Javascript script to
	// redirect Gecko-based browsers to the XUL-based interface
	if(!intval($_GET['noxul']))
		echo '<script type="text/javascript">if(navigator.userAgent.indexOf("Gecko") >= 0) document.location.href = "book.xul.php?book=' . htmlspecialchars($alias, ENT_QUOTES) . '";</script>';
	
	echo '<frameset cols="256,*">';
	echo '<frame src="tocfrm.php?book=' . htmlspecialchars($alias, ENT_QUOTES) . '" name="navigation"/>';
	echo '<frame src="page.php/' . htmlspecialchars($alias, ENT_QUOTES) . '/' . $book->default_link() . '" name="main"/>';
	echo '<noframes><body>A frames-capable web browser is required.</body></noframes>';
	echo '</frameset>';

	echo '</html>';
?>
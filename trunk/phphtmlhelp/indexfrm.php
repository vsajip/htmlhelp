<?php

$title = 'Index';
$id = 'index';
$search_button = 'Find';
require 'inc/frmheader.inc.php';

	if(isset($query))
	{
		$entries = $book->index($query);
		if(count($entries))
		{
			echo '<ul class="list">';
			foreach($entries as $entry)
			{
				list($term, $path) = $entry;
				echo '<li><a href="' . htmlspecialchars($path, ENT_QUOTES) .'">' . htmlspecialchars($term, ENT_NOQUOTES) . '</a></li>';
			}
			echo '</ul>';
		}
	}
	
require 'inc/frmfooter.inc.php';
?>

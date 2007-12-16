<?php

$title = 'Search';
$id = 'search';
$search_button = 'Go';
require 'inc/frmheader.inc.php';

	if($query)
	{
		$entries = $book->search($query);
		if(count($entries))
		{
			echo '<ul class="list">';
			foreach($entries as $entry)
			{
				list($title, $path) = $entry;
				echo '<li><a href="' . htmlspecialchars($path, ENT_QUOTES) .'">' . htmlspecialchars($title, ENT_NOQUOTES) . '</a></li>';
			}
			echo '</ul>';
		}
	}

require 'inc/frmfooter.inc.php';
?>

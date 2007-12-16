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

	echo '<script src="js/tocfrm.js"/>';

	echo '<button label="Sync" oncommand="onButtonCommand(event);"/>';
						
	echo '<tree id="tree" flex="1" seltype="single" hidecolumnpicker="true" onselect="onTocSelect(event, \'' . htmlspecialchars($alias, ENT_QUOTES) . '\');">';

	echo '<treecols>';
	echo '<treecol id="name" hideheader="true" primary="true" flex="1"/>';
	echo '</treecols>';

	function walk_toc_entries($parent_no = 0)
	{
		global $book;
		
		$entries = $book->get_toc_entries($parent_no);
		if(count($entries))
		{
			echo '<treechildren>';
			foreach($entries as $number => $entry)
			{
				list($title, $link, $nchildren) = $entry;
				
				if($nchildren)
					echo '<treeitem container="true">';
				else
					echo '<treeitem>';
					
				echo '<treerow>';
				echo '<treecell label="' . htmlspecialchars($title, ENT_QUOTES) . '" value="' . htmlspecialchars($link, ENT_QUOTES) . '"/>';
				echo '</treerow>';
		
				walk_toc_entries($number);
				
				echo '</treeitem>';
			}
			echo '</treechildren>';
		}
	}

	walk_toc_entries(0);

	echo '</tree>';

	echo '</window>';
?>

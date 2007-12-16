<?php

$title = 'Table of Contents';
$id = 'toc';
// TODO: Add filtering to TOC
//$search_button = 'Filter';
require 'inc/frmheader.inc.php';

$toc_nos = array();
foreach(explode(' ', $_GET['toc_nos']) as $toc_no)
	$toc_nos[intval($toc_no)] = TRUE;

$linage = array();

function walk_toc_entries($parent_no = 0)
{
	global $alias, $book, $toc_nos, $linage;
	
	$entries = $book->get_toc_entries($parent_no);
	if(count($entries))
	{
		echo '<ul class="tree">';
		foreach($entries as $number => $entry)
		{
			list($name, $link, $nchildren) = $entry;

			if($nchildren)
			{
				if($toc_nos[$number])
					echo '<li class="expanded">';
				else
					echo '<li class="collapsed">';
			}
			else
				echo '<li class="single">';
		
			array_push($linage, $number);
			
			if($toc_nos[$number] || !$nchildren)
				echo '<a href="' . $link . '">';
			else
				// See also http://htmlhelp.com/faq/html/frames.html#frame-update2 
				echo '<a href="../../tocfrm.php?book=' . htmlspecialchars($alias, ENT_QUOTES) . '&amp;toc_nos=' . implode('+', $linage) . '" target="_self" onclick="top.main.location=\'' . htmlspecialchars($base . $link, ENT_QUOTES) . '\';">';
			echo htmlspecialchars($name, ENT_NOQUOTES) . '</a>';
			
			if($toc_nos[$number] && $nchildren)
				walk_toc_entries($number);
			
			array_pop($linage);
			
			echo '</li>';
		}
		echo '</ul>';
	}
}

walk_toc_entries(0);
	
require 'inc/frmfooter.inc.php';
?>

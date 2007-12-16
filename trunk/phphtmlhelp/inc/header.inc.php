<?php
require_once 'inc/config.inc.php';
require_once 'lib/book_catalog.lib.php';

header('Content-Type: text/html; charset=' . $internal_encoding);

// FIXME: deal with browser chaching

echo '<?xml version="1.0" encoding="' . $internal_encoding . '"?>';	
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=<?php echo $internal_encoding; ?>"/>
	<title>HTML Help Books</title>
	<link href="css/default.css" type="text/css" rel="stylesheet"/>
</head>
<body>
	<div class="header">HTML Help Books</div>
	
	<div id="tags" class="sidebox">
		<span class="title">Tags</span>
		<table>
			<tr>
				<th class="count">#</th>
				<th class="tag">Tag</th>
			</tr>
<?php
$catalog = new BookCatalog();
$tags = $catalog->count_tags();
foreach($tags as $tag => $tag_count)
{
?>
			<tr >
				<td class="count"><?php echo $tag_count; ?></td>
				<td class="tag"><a href="books.php?tag=<?php echo htmlspecialchars($tag, ENT_QUOTES); ?>"><?php echo htmlspecialchars($tag, ENT_NOQUOTES); ?></a></td>
			</tr>
<?php
}
?>
			<tr>
				<td class="count"></td>
				<td class="tag"><a href="books.php">all</a></td>
			</tr>
		</table>
	</div>

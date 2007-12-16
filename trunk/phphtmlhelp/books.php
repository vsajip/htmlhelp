<?php
require 'inc/header.inc.php';
?>
	<div class="content">
<?php
	if($tag = $_GET['tag'])
		$books = $catalog->enumerate_books_by_tag($tag);
	else	
		$books = $catalog->enumerate_books();	
	if(count($books))
	{
?>
		<ul class="list">
<?php
		foreach($books as $book_alias => $book_title)
		{
?>
			<li><a href="book.php?book=<?php echo htmlspecialchars($book_alias, ENT_QUOTES); ?>"><?php echo htmlspecialchars($book_title, ENT_NOQUOTES);?></a></li>
<?php
		}
?>
		</ul>
<?php
	}
	else
	{
?>
		<p class="warning">No book found.</p>
<?php
	}
?>
	</div>
<?php
require 'inc/footer.inc.php';
?>

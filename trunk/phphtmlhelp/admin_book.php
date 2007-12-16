<?php

require_once 'inc/config.inc.php';

require_once 'lib/book_catalog.lib.php';
require_once 'lib/book_builder.lib.php';

require 'inc/admin_auth.inc.php';

require 'inc/header.inc.php';

$catalog = new BookCatalog();

$book_id = $_POST['book'];

$action = $_POST['action'];
if(isset($book_id) && isset($action))
{
	$book = & new BookBuilder(intval($book_id));
	switch($action)
	{
		case 'set_title':
			$title = $_POST['title'];
			$book->set_title($title);
			break;

		case 'delete';
			$book->delete();
			$book_id = NULL;
			break;
			
		case 'set_metadata':
			$name = $_POST['name'];
			$value = $_POST['value'];
			$book->set_metadata($name, $value);
			break;
	}
}
?>
	<div class="content">

<?php
if(!isset($book_id))
{
?>
		<h2>Edit</h2>

		<form action="admin_book.php" method="post">
			<p>
				<select name="book" size="20">
<?php
	$books = $catalog->enumerate_book_ids();	
	foreach($books as $book_id => $book_title)
	{
?>
					<option value="<?php echo $book_id; ?>"><?php echo htmlspecialchars($book_title, ENT_NOQUOTES); ?></option>';
<?php
	}
?>
				</select>
				<br/>
				<button type="submit">Edit</button>
			</p>
		</form>
<?php
}
else
{
		$book = & new Book($book_id);
?>
		<h2>Book "<?php echo htmlspecialchars($book->title(), ENT_NOQUOTES); ?>"</h2>

		<h3>Title</h3>			
		<form action="admin_book.php" method="post">
			<p>
				<input type="hidden" name="book" value="<?php echo $book->id; ?>"/>
				<input type="text" name="title" value="<?php echo htmlspecialchars($book->title(), ENT_QUOTES); ?>"/>
				<button type="submit" name="action" value="set_title">Set title</button>
			</p>
		</form>
			
		<h3>Metadata</h3>
	
<?php
	$names = array(
		"name", 
		"version", 
		"language", 
		"date"
	);
	foreach($names as $name)
	{
?>
		<form action="admin_book.php" method="post">
			<p>
				<input type="hidden" name="book" value="<?php echo $book->id; ?>"/>
				<input type="hidden" name="name" value="<?php echo $name; ?>"/>
				<input type="text" name="value" value="<?php echo htmlspecialchars($book->metadata($name), ENT_QUOTES); ?>"/>
				<button type="submit" name="action" value="set_metadata">Set <?php echo $name; ?></button>
			</p>
		</form>
<?php
	}
?>

		<h3>Miscellaneous</h3>			
		<form action="admin_book.php" method="post">
			<p>
				<input type="hidden" name="book" value="<?php echo $book->id; ?>"/>
				<button type="submit" name="action" value="delete">Delete</button>
			</p>
		</form>
<?php
}
?>
	</div>
<?php
require_once 'inc/footer.inc.php';
?>

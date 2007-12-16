<?php

require_once 'inc/config.inc.php';

require_once 'lib/book_catalog.lib.php';

require 'inc/admin_auth.inc.php';

require 'inc/header.inc.php';

$catalog = new BookCatalog();

$action = $_POST['action'];
if(isset($action))
{
	echo '<div class="content result">';

	// disable memory and time limits, necessary for some administration tasks
	ini_set('memory_limit','-1');
	if(!intval(ini_get('safe_mode')))
		set_time_limit(0);

	echo "<pre>\n";
	$start_time = time();
	switch($action)
	{
		case 'import':
			$files = $_POST['files'];
			if(isset($files))
				foreach($files as $file)
				{
					echo "Importing " . htmlspecialchars($file, ENT_NOQUOTES) . "\n";
					ob_flush();
					flush();
					$catalog->import_book($admin_directory . "/" .$file);
				}
			break;
		
		case 'upload':
			$file = $_FILES['file']['tmp_name'];
			if(isset($file) and is_uploaded_file($file))
			{
				echo "Importing " . htmlspecialchars($_FILES["file"]["name"], ENT_NOQUOTES) . "\n";
				ob_flush();
				flush();
				$catalog->import_book($file);
			}
			break;
		
		case 'index':
			$book_ids = $_POST['books'];
			if(isset($book_ids))
				foreach($book_ids as $book_id)
				{
					$book = $catalog->get_book_by_id($book_id);
					$title = $book->title();
					echo "Indexing " . htmlspecialchars($title, ENT_NOQUOTES) . "\n";
					ob_flush();
					flush();
					$book->index_fulltext();
				}
			break;
		
		case 'delete';
			$book_ids = $_POST['books'];
			if(isset($book_ids))
				foreach($book_ids as $book_id)
				{
					$book = $catalog->get_book_by_id($book_id);
					$title = $book->title();
					echo "Deleting " . htmlspecialchars($title, ENT_NOQUOTES) . "\n";
					$book->delete();
				}
			break;
	}

	$finish_time = time();
	$ellapsed_time = $finish_time - $start_time;
	if($ellapsed_time)
		echo "Ellapsed time: $ellapsed_time sec\n";

	echo "</pre>";
	echo '</div>';
}

?>

	<div class="content">

		<h2>Books</h2>

<?php 
	if($admin_directory) { 
?>
		<h3>Import</h3>
		<form action="admin_books.php" method="post">
			<p>
				<select name="files[]" multiple="multiple" size="20">
<?php
		$dir = dir($admin_directory);
		$ext = '.tgz';
		$entries = array();
		while(false !== ($entry = $dir->read()))
			if(substr($entry, -strlen($ext)) == $ext)
				$entries[] = $entry;
		natcasesort($entries);
		foreach($entries as $entry)
			echo '<option value="' . $entry . '">' . substr($entry, 0, -strlen($ext)) . '</option>';
?>
				</select>
				<br/>
				<button type="submit" name="action" value="import">Import books</button>
			</p>
		</form>

<?php
	} 
?>
		<h3>Upload</h3>
		<form enctype="multipart/form-data" action="admin_books.php" method="post">
			<p>
<?php
				$MAX_FILE_SIZE = ini_get('upload_max_filesize');
				if(substr($MAX_FILE_SIZE, -1) == 'M')
					$MAX_FILE_SIZE = intval(substr($MAX_FILE_SIZE, 0, -1))*1024*1024;
				if($MAX_FILE_SIZE)
					echo '<input type="hidden" name="MAX_FILE_SIZE" value="' . $MAX_FILE_SIZE . '"/>';
?>
				<input type="file" name="file"/>
				<button type="submit" name="action" value="upload">Upload book</button>
			</p>
		</form>

		<h3>Edit</h3>
		
		<form action="admin_books.php" method="post">
			<p>
				<select name="books[]" multiple="multiple" size="20">
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
				<button type="submit" name="action" value="delete">Delete books</button>
				<button type="submit" name="action" value="index">Index books</button>
			</p>
		</form>
	</div>
<?php
require_once 'inc/footer.inc.php';
?>

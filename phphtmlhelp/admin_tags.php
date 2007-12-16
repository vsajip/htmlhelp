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
	switch($action)
	{
		case 'add':
			$tags = $_POST['tags'];
			$tags = explode(' ', $tags);
			$result = $catalog->add_tags($tags);
			echo "$result tags added";
			break;
			
		case 'delete':
			$tags = $_POST['tags'];
			$result = $catalog->delete_tags($tags);
			echo "$result tags deleted";
			break;			
			
		case 'tag';
			$aliases = $_POST['aliases'];
			$tags = $_POST['tags'];
			$result = $catalog->tag_books($aliases, $tags);
			echo "$result tags applied";
			break;
			
		case 'untag';
			$aliases = $_POST['aliases'];
			$tags = $_POST['tags'];
			$result = $catalog->untag_books($aliases, $tags);
			echo "$result tags removed";
			break;
	}
	echo '</div>';
}
?>

	<div class="content">		

		<h2>Tags</h2>
		
		<form action="admin_tags.php" method="post">
			<p>
				<input type="text" name="tags"/>
				<button type="submit" name="action" value="add">Add tag</button>
			</p>
		</form>
		
		<form action="admin_tags.php" method="post">
			<table>
				<tr>
					<th>Tags</th>
					<th>Aliases</th>
				</tr>
				<tr>
					<td>
						<select name="tags[]" multiple="multiple" size="25">
<?php
	$tags = $catalog->enumerate_tags();
	foreach($tags as $tag)
	{
?>
							<option value="<?php echo htmlspecialchars($tag, ENT_QUOTES); ?>"><?php echo htmlspecialchars($tag, ENT_NOQUOTES); ?></option>
<?php
	}
?>
						</select>
					</td>
					<td>
						<select name="aliases[]" multiple="multiple" size="25">
<?php
	$aliases = $catalog->enumerate_aliases();	
	foreach($aliases as $alias)
	{
?>
							<option value="<?php echo htmlspecialchars($alias, ENT_QUOTES); ?>"><?php echo htmlspecialchars($alias, ENT_NOQUOTES); ?></option>
<?php
	}
?>
						</select>
					</td>
				</tr>
				<tr>
					<td>
						<button type="submit" name="action" value="delete">Delete tag</button>
					</td>
					<td>
						<button type="submit" name="action" value="tag">Tag</button>
						<button type="submit" name="action" value="untag">Untag</button>
					</td>
				</tr>
			</table>
		</form>
	</div>
<?php
require_once 'inc/footer.inc.php';
?>
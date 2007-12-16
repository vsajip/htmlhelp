<?php

require_once 'inc/config.inc.php';
require_once 'lib/book_catalog.lib.php';

require 'inc/admin_auth.inc.php';

require 'inc/header.inc.php';

?>
	<div class="content">
		<table>
			<tr>
				<th>Alias</th>
				<th>Book hits</th>
				<th>Page hits</th>
			</tr>
<?php
		$stats = $catalog->get_hit_stats();
		foreach($stats as $item)
		{
			list($alias, $book_hits, $page_hits) = $item;
?>
			<tr>
				<td><?php echo htmlspecialchars($alias, ENT_NOQUOTES); ?></td>
				<td><?php echo $book_hits; ?></td>
				<td><?php echo $page_hits; ?></td>
			</tr>
<?php
		}
?>
		</table>
	</div>
<?php
require_once 'inc/footer.inc.php';
?>

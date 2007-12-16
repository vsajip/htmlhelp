<?php

$db_version_major = 1; 
$db_version_minor = 4;

mysql_connect($db_server, $db_username, $db_password);
mysql_select_db($db_database);
mysql_query("SET NAMES '$internal_encoding'");

$major = 0; 
$minor = 0;
if(
	($result = mysql_query('SELECT major, minor FROM version')) && 
	mysql_num_rows($result) && 
	(list($major, $minor) = mysql_fetch_row($result)) &&
	($major == $db_version_major && $minor == $db_version_minor)
)
	return;

require_once('lib/mysql_util.lib.php');

if($major != $db_version_major)
{
	mysql_import_dump('sql/create.sql');
	mysql_import_dump('sql/tags.sql');	
	mysql_import_dump('sql/book_tags.sql');	
}
elseif($minor < $db_version_minor)
{
	mysql_import_dump('sql/update.sql', TRUE);
}

?>

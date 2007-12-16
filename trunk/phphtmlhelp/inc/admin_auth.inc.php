<?php

require_once 'inc/config.inc.php';

// Disable caching
header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
header("Expires: Mon, 26 Jul 1997 05:00:00 GMT"); // Date in the past

// authentication must be done before any actual output
$password = $_COOKIE['Password'];
if($password == $admin_password)
	$authenticated = TRUE;
else
{
	setcookie("Password", "", time() - 3600);
	// TODO: redirect back to originating page
	header('Location: http://' . $_SERVER['HTTP_HOST'] . dirname($_SERVER['REQUEST_URI']) . '/admin_login.php');
	exit;
}
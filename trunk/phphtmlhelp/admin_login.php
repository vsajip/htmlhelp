<?php

require_once 'inc/config.inc.php';

$password = $_POST['password'];
if($password == $admin_password)
{
	setcookie('Password', $password);
	header('Location: http://' . $_SERVER['HTTP_HOST'] . dirname($_SERVER['REQUEST_URI']) . '/admin.php');
}

require 'inc/header.inc.php';

?>
	<div class="content">		
		<h2>Login</h2>
		<form action="admin_login.php" method="post">
			<p>
				<input type="password" name="password"/>
				<br/>
				<input type="submit" value="Login">
			</p>
		</form>
	</div>
<?php
require_once 'inc/footer.inc.php';
?>
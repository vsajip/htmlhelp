<?php

// Creates a directory with a unique name at the specified with the specified 
// prefix.
//
// Returns directory name on success, false otherwise
//
// Taken from comments in http://pt.php.net/manual/en/function.tempnam.php
function tmpdir($path, $prefix)
{
       // Use PHP's tmpfile function to create a temporary
       // directory name. Delete the file and keep the name.
       $tempname = tempnam($path,$prefix);
       if (!$tempname)
               return false;

       if (!unlink($tempname))
               return false;

       // Create the temporary directory and returns its name.
       if (mkdir($tempname))
               return $tempname;

       return false;
}

function gzdecode($string)
{
	# FIXME: verify header here
	return gzinflate(substr($string, 10, -4));
}

?>
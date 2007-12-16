<?php
/*
 * Replacements for some of the mbstring extension functions
 */

if(!function_exists('mb_convert_encoding')) {

$_mb_encodings = array(
	'ASCII' => 'ASCII',
	'ISO8859-1' => 'ISO-8859-1',
	'ISO8859-15' => 'ISO-8859-15',
	'UTF-8' => 'UTF-8',
);

// canonize encoding
function _mb_encoding($encoding)
{
	global $_mb_encodings;
	return $_mb_encodings[strtoupper($encoding)];
}

function mb_convert_encoding($str, $to_encoding, $from_encoding)
{
	if(function_exists('iconv'))
		return iconv($from_encoding, $to_encoding, $str);

	if(function_exists('recode_string'))
		return recode_string("$from_encoding..$to_encoding", $str);

	$to_encoding = _mb_encoding($to_encoding);
	$from_encoding = _mb_encoding($from_encoding);
	
	if($from_encoding == 'ISO-8859-1' && $to_encoding == 'UTF-8')
		return utf8_encode($str);
	if($from_encoding == 'UTF-8' && $to_encoding == 'ISO-8859-1')
		return utf8_decode($str);

	// replace higher ASCII codes by a question mark
	return preg_replace('/[\x80-\xff]/', '?', $str);
}

}
?>

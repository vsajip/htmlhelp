<?php

require_once 'PHPUnit.php';

require_once 'lib/fulltext_tokenizer.lib.php';


class TokenizerTest extends PHPUnit_TestCase
{
	function setup()
	{
		$this->tokenizer = new Fulltext_Utf8_Tokenizer(); 
	}
	
	function testTokenize()
	{
		$testcases = array(
			// empty
			"" => array(),

			// words
			"pre post" => array("pre", "post"),
			"pre/post" => array("pre", "post"),
			"pre,post" => array("pre", "post"),
			"pre. post" => array("pre", "post"),
			" pre  post " => array("pre", "post"),

			// acronyms
			"pre A.B. post" => array("pre", "A.B.", "post"),
			"pre C.D.E., post" => array("pre", "C.D.E.", "post"),
			"pre X.Y.Z.. post" => array("pre", "X.Y.Z.", "post"),

			// emails
			"pre simple@email.com post" => array("pre", "simple@email.com", "post"), 
			"pre strange_email.address@somewhere1.com post" => array("pre", "strange_email.address@somewhere1.com", "post"), 

			// versions
			"package-1.2.3.4a.ext" => array("package", "1.2.3.4a", "ext"),

			// ip numbers
			"pre 127.0.0.1 post" => array("pre", "127.0.0.1", "post"),
			"pre 196.168.0.1. post" => array("pre", "196.168.0.1", "post"),

			// numbers
			"pre 10 post" => array("pre", "10", "post"),
			"pre 10, 20, 30 post" => array("pre", "10", "20", "30", "post"),
			"pre .2 post" => array("pre", ".2", "post"),
			"pre 3.456789E-123 post" => array("pre", "3.456789E-123", "post"),
			"pre 10+20 post" => array("pre", "10", "20", "post"),
			"pre 30*40 post" => array("pre", "30", "40", "post"),
			"pre 50/60 post" => array("pre", "50", "60", "post"),
			"pre 0x1234 post" => array("pre", "0x1234", "post"),
			"pre 10101010b post" => array("pre", "10101010b", "post"),

			// dates
			"pre 1234-12-23 post" => array("pre", "1234-12-23", "post"),
			"pre 07/06/00 post" => array("pre", "07/06/00", "post"),

			// Latin-1 characters
			"Eagle \xC3\x80guia" => array("Eagle", "\xC3\x80guia"),
		);
		foreach($testcases as $string => $result)
			$this->assertEquals($result, $this->tokenizer->tokenize($string));
	}
	
	function testSplit()
	{
		$testcases = array(
			"" => array(),

			// white space
			" \t\r\n" => array(),
			
			// U+00A0 NO-BREAK SPACE
			"\xC2\xA0" => array(),

			"  a house" => array("a", "house"),
			" a   house " => array("a", "house"),
			"a  house" => array("a", "house"),
		);
		foreach($testcases as $string => $result)
			$this->assertEquals($result, $this->tokenizer->split($string));
	}
}


$testcases = array(
	'TokenizerTest',
);
foreach($testcases as $testcase)
	echo PHPUnit::run(new PHPUnit_TestSuite($testcase))->toString();

?>

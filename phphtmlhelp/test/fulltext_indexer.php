<?php

require_once 'PHPUnit.php';

require_once 'lib/fulltext_index.lib.php';
require_once 'lib/fulltext_indexer.lib.php';


class IndexStub extends Fulltext_Index
{
}

class HtmlIndexerTest extends PHPUnit_TestCase
{
	function setUP()
	{
		$this->index = new IndexStub();
		$this->indexer = new Fulltext_HtmlIndexer($this->index);
	}
	
	function testExtractEncoding()
	{
		$testcases = array(
			"" => NULL,

			// Based from http://search.cpan.org/~bjoern/HTML-Encoding-0.52/lib/HTML/Encoding.pm
			"<?xml version='1.0'>"                    => NULL,
			"<?xml version='1.0' encoding='utf-8'?>"  => 'utf-8',
			"<?xml encoding='utf-8'?>"                => 'utf-8',
			"<?xml encoding=\"utf-8\"?>"              => 'utf-8',
			"<?xml foo='bar' encoding='utf-8'?>"      => 'utf-8',
			"<?xml encoding='a' encoding='b'?>"       => 'a',
			"<?xml-stylesheet encoding='utf-8'?>"     => NULL,
			" <?xml encoding='utf-8'?>"               => NULL,
			"<?xml encoding = 'utf-8'?>"              => 'utf-8',
			"<?xml version='1.0' encoding=utf-8?>"    => NULL,
			"<?xml x='encoding=\"a\"' encoding='b'?>" => 'b',

			'<META http-equiv="Content-Type" content="text/html">'                           => NULL,
			'<META http-equiv="Content-Type" content="text/html,text/plain;charset=utf-8">'  => NULL,
			'<META http-equiv="Content-Type" content="text/html;charset=">'                  => NULL,
			'<META http-equiv="Content-Type" id="test" content="text/html;charset=utf-8">'   => 'utf-8',
			'<META http-equiv="Content-Type" content="text/html;charset=\'utf-8\'">'         => 'utf-8',
			'<META http-equiv="Content-Type" content=\'text/html;charset="UTF-8"\'>'         => 'UTF-8',
			'<META http-equiv="Content-Type" content="text/html;charset=&quot;UTF-8&quot;">' => 'UTF-8',

		);
		foreach($testcases as $html => $title)
			$this->assertEquals($title, $this->indexer->extract_encoding($html, NULL), $html);
	}

	function testDecode()
	{
		$testcases = array(
			// Basic HTML entities
			'&amp;' => '&',
			'&lt;' => '<',
			'&gt;' => '>',
			'&quot;' => '"',

			// Latin capital letter A with grave (U+00C0)
			"&Agrave;" => "\xC3\x80",
			"&#192;" => "\xC3\x80",
			"&#xC0;" => "\xC3\x80",
			"\xC0" => "\xC3\x80",
		);
		foreach($testcases as $html => $title)
			$this->assertEquals($title, $this->indexer->decode_html($html));
	}

	function testExtractTitle()
	{
		$testcases = array(
			"before<title></title>after" => "",
			"<title>Simple</title>" => "Simple",
			"<Title>Ignore case</TITLE>" => "Ignore case",
			"<title id=\"id123\">Attributes</title>" => "Attributes",
			"<title id=\"id123\">Html entities: &amp;&lt;&gt;</title >" => "Html entities: &<>",
			"<title\n\n>\nNewlines\n</title\n\n>" => "\nNewlines\n",
		);
		foreach($testcases as $html => $title)
			$this->assertEquals($title, $this->indexer->extract_title($html));
	}

	function testExtractBody()
	{
		$testcases = array(
			"before<body></body>after" => "",
			"<body>Simple</body>" => "Simple",
			"<Body>Ignore case</BODY>" => "Ignore case",
			"<body id=\"id123\">Attributes</body>" => "Attributes",
			"<body id=\"id123\">Html entities: &amp;&lt;&gt;</body >" => "Html entities: &<>",
			"<body><b class=\"bold\">Tags</b></body\n\n>" => " Tags ",
			"<body\n\n>\nNewlines\n</body\n\n>" => "\nNewlines\n",
		);
		foreach($testcases as $html => $body)
			$this->assertEquals($body, $this->indexer->extract_body($html));
	}
}

class IndexerFactoryTest extends PHPUnit_TestCase
{
	var $index;

	function setUp()
	{
		$this->index = new IndexStub();
	}

	function tearDown()
	{
		unset($this->index);
	}

	function testIndexer()
	{
		$testcases = array(
			'abc.txt' => 'Fulltext_TextIndexer',
			'abc.htm' => 'Fulltext_HtmlIndexer',
			'abc.html' => 'Fulltext_HtmlIndexer',
		);
		foreach($testcases as $path => $class)
			$this->assertTrue(is_a(Fulltext_indexer_factory($path, $this->index), $class), $class);
	}
}

$testcases = array(
	'HtmlIndexerTest',
	'IndexerFactoryTest',
);
foreach($testcases as $testcase)
	echo PHPUnit::run(new PHPUnit_TestSuite($testcase))->toString();

?>

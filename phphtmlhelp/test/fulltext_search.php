<?php

require_once 'PHPUnit.php';

require_once 'lib/fulltext_index.lib.php';
require_once 'lib/fulltext_search.lib.php';


class IndexStub extends Fulltext_Index
{
	function IndexStub($pages)
	{
		parent::Fulltext_Index('ASCII');
		
		foreach($pages as $page => $lexemes)
			foreach($lexemes as $lexeme)
			{
				if(!isset($this->lexemes[$lexeme]))
					$this->lexemes[$lexeme] = array();
				$this->lexemes[$lexeme][] = $page;
			}
	}

	function search_lexeme($lexeme)
	{
		$entries = array();
		if(isset($this->lexemes[$lexeme]))
			foreach($this->lexemes[$lexeme] as $page)
				$entries[] = array($page);
		return new Fulltext_SearchResult($entries);
	}
}

class SearchTest extends PHPUnit_TestCase
{
	var $searchable;

	function setUp()
	{
		$this->searchable = new IndexStub(array(
			'felines' => array('cat', 'lion'),
			'domestic' => array('cat', 'dog'),
		));
	}

	function tearDown()
	{
		unset($this->searchable);
	}

	function testMissing()
	{
		$this->assertEquals(
			array(),
			$this->searchable->search('mouse')); 
	}

	function testSingle()
	{
		$this->assertEquals(
			array(array('felines')),
			$this->searchable->search('lion'));
		$this->assertEquals(
			array(array('felines'), array('domestic')),
			$this->searchable->search('cat'));
	}

	function testMultiple()
	{
		$this->assertEquals(
			array(array('felines')), 
			$this->searchable->search('cat lion'));
		$this->assertEquals(
			array(), 
			$this->searchable->search('lion dog'));
	}
}


$testcases = array(
	'SearchTest',
);
foreach($testcases as $testcase)
	echo PHPUnit::run(new PHPUnit_TestSuite($testcase))->toString();

?>

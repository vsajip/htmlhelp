<?php

require_once 'lib/fulltext_tokenizer.lib.php';
require_once 'lib/fulltext_search.lib.php';

// Index interface
class Fulltext_Index
{
	var $encoding;
	var $tokenizer;

	function Fulltext_Index($encoding = 'UTF-8')
	{
		$this->encoding = $encoding;
		$this->tokenizer = & Fulltext_tokenizer_factory($index->encoding);
	}

	// Enumerate items to be indexed
	function enumerate_items() {}
	
	// Index a item
	function index_item(&$item) {}
	
	// Indexing start callback
	function handle_start() {}	
	
	// Item (e.g., a new page) begin callback
	function handle_item_start(&$item) {}

	// Set item title callback
	function handle_item_title($title) {}

	// Lexemes callback
	function handle_item_lexemes(&$lexemes) {}

	// Item finish callback
	function handle_item_end() {}
	
	// Indexing finish callback
	function handle_end() {}

	// Reindex
	function index()
	{
		$this->handle_start();
		$items = $this->enumerate_items();
		foreach($items as $item)
		{
			$this->handle_item_start($item);
			$this->index_item($item);
			$this->handle_item_end();
		}
		$this->handle_end();
	}
	
	// Return items containing this lexeme
	function search_lexeme($lexeme) {}
	
	function search($query)
	{
		$search = & Fulltext_Search_parse($query, $this->tokenizer);
		$result = & $search->apply($this);
		return $result->enumerate();
	}
}

?>

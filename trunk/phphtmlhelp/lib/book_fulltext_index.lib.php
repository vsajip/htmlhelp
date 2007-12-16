<?php

require_once 'inc/mysql.inc.php';
require_once 'lib/mysql_util.lib.php';
require_once 'lib/fulltext_index.lib.php';
require_once 'lib/fulltext_indexer.lib.php';

class Book_Fulltext_SearchResult extends Fulltext_SearchResult
{
	function enumerate()
	{
		return $this->entries;
	}	
}

class Book_Fulltext_Index extends Fulltext_Index
{
	var $book_id;
	
	// current page
	var $page_no;

	// whole index
	var $lexemes;
	
	function Book_Fulltext_Index($book_id)
	{
		global $internal_encoding;		
		parent::Fulltext_Index($internal_encoding);
		
		$this->book_id = $book_id;
	}
	
	function enumerate_items()
	{
		$result = mysql_query("
			SELECT no
			FROM page 
			WHERE book_id = $this->book_id
		") or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error() . "\n");
		return mysql_fetch_fields($result);
	}
	
	function index_item($page_no)
	{
		$result = mysql_query("
			SELECT path, compressed, content
			FROM page 
			WHERE book_id = $this->book_id
			AND no = $page_no
		") or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error() . "\n");
		list($path, $compressed, $content) = mysql_fetch_row($result);
		
		// Heartbeat
		echo "  indexing $path\n";
		ob_flush();
		flush();	
		
		if($compressed)
			$content = gzdecode($content);
		
		if(($indexer = & Fulltext_Indexer_factory($path, $this)) !== NULL)
			$indexer->feed($content);
	}
	
	function handle_start()
	{
		parent::handle_start();
		
		mysql_query("DELETE FROM lexeme_page WHERE book_id = $this->book_id");
		mysql_query("UPDATE page SET title='' WHERE book_id = $this->book_id");

		$this->lexemes = array();
	}
	
	function handle_item_start($page_no)
	{
		$this->page_no = $page_no;
	}
	
	function handle_item_title($title) 
	{
		mysql_query("
			UPDATE page
			SET title='" . mysql_escape_string($title) . "'
			WHERE book_id = $this->book_id 
				AND no = $this->page_no
		") or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error() . "\n");
	}
	
	function handle_item_lexemes(&$lexemes)
	{
		foreach($lexemes as $lexeme)
			$this->lexemes[substr($lexeme, 0, 31)][$this->page_no] += 1;
	}

	function handle_item_end()
	{
		$this->page_no = NULL;
	}

	function handle_end()
	{
		if(!count($this->lexemes))
			return;
		
		// TODO: store lexeme positions instead of lexeme counts
		$values = array();
		foreach($this->lexemes as $lexeme => $pages)
		{
			arsort($pages, SORT_NUMERIC);
			$pages_blob = '';
			foreach($pages as $page_no => $count)
				$pages_blob .= pack("vC", $page_no, min($count, 255));
			$values[] = '(' . $this->book_id . ',"' . mysql_escape_string($lexeme) . '","' . mysql_escape_string($pages_blob) . '")';
		}
	
		mysql_extended_insert('lexeme_page', '(book_id, lexeme, pages)', $values)		
		or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
		
		$this->lexemes = NULL;
	}
	
	function search_lexeme($lexeme)
	{
		$result = mysql_query(
			"SELECT pages " . 
			"FROM lexeme_page " .
			"WHERE book_id = $this->book_id " .
				"AND lexeme='" . mysql_escape_string(substr($lexeme, 0, 31)) . "'" 
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error() . "\n");
		list($pages_blob) = mysql_fetch_row($result);
		
		$pages = array();
		$pos = 0;
		$len = strlen($pages_blob);
		while($pos < $len)
		{
			$data = unpack("vpage_no/Ccount", substr($pages_blob, $pos, 3));
			$pages[$data['page_no']] = $data['count'];
			$pos += 3;
		}
		
		return new Fulltext_SearchResult($pages);
	}
	
	function search($query)
	{
		$entries = parent::search($query);
		
		// TODO: optimize this using temporary tables
		$pages = array();
		foreach($entries as $page_no => $score)
		{
			$result = mysql_query(
				"SELECT title, path " . 
				"FROM page " .
				"WHERE book_id = $this->book_id " .
					"AND no = $page_no" 
			) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error() . "\n");
			$pages[] = mysql_fetch_row($result);
		}
		
		return $pages;
	}
}

?>

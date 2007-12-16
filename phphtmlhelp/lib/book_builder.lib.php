<?php

require_once 'lib/book.lib.php';

class BookBuilder extends Book
{
	var $commited;
	
	var $last_page_no;
	var $last_toc_entry_no;
	var $last_index_entry_no;
	
	// Constructor
	function BookBuilder($id = NULL)
	{
		if(is_null($id))
		{
			// TODO: allow to upgrade books
			mysql_query("INSERT INTO book () VALUES ()");
			$id = mysql_insert_id();

			$this->commited = FALSE;
			register_shutdown_function(array(&$this, "_BookBuilder"));
		}

		$this->Book($id);

		mysql_query(
			"CREATE TEMPORARY TABLE temp_index_entry (
			  term varchar(255) NOT NULL,
			  path varchar(255) NOT NULL,
			  anchor varchar(255) NOT NULL
			)"
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error() . "\n");
		
		$this->last_page_no = 0;	
		$this->last_toc_entry_no = 0;	
		$this->last_index_entry_no = 0;	
	}
	
	// Destructor
	function _BookBuilder()
	{
		if(!$this-commited)
		{
			// revert all changes
			$this->delete();
		}
	}

	function set_title($title)
	{
		mysql_query(
			'UPDATE book ' .
			'SET title = "' . mysql_escape_string($title) . '" ' .
			'WHERE id = ' . $this->id 
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
		
		// keep book table sorted by title to speed up frequent ordering
		mysql_query(
			'ALTER TABLE book ORDER BY title'
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
	}
	
	// Add a book page.
	//		
	// All pages should be added before any link can be added, as links 
	// are internally stored as a page reference plus an anchor.
	function add_page($path, $content)
	{
		// Heartbeat
		echo "  adding $path\n";
		ob_flush();
		flush();	

		// gzip content
		$gzcontent = gzencode($content);
		if(strlen($gzcontent) < strlen($content))
		{
			$compressed = 1;
			$content = & $gzcontent;
		}
		else
			$compressed = 0;
		
		$this->last_page_no += 1;
		mysql_query(
			'INSERT ' .
			'INTO page ' . 
			'(book_id, no, path, compressed, content) ' . 
			'VALUES (' . 
				$this->id . ', ' .
				$this->last_page_no . ', ' .
				'"' . mysql_escape_string($path) . '", ' .
				$compressed . ', ' .
				'"' . mysql_escape_string($content) . '")' 
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
	}
	
	// Split a link into a page reference plus anchor pair
	function __split_link($link)
	{
		$pos = strpos($link, '#');
		if($pos === FALSE)
		{
			$path = $link;
			$anchor = '';
		}
		else
		{
			$path = substr($link, 0, $pos);
			$anchor = substr($link, $pos + 1);
		}
		
		return array($path, $anchor);
	}
	function _split_link($link)
	{
		list($path, $anchor) = $this->__split_link($link);
		
		$result = mysql_query(
			'SELECT no ' .
			'FROM page ' .
			'WHERE book_id = ' . $this->id . ' ' .
				'AND path = "' . mysql_escape_string($path) . '"'
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
		if(mysql_num_rows($result))
			list($page_no) = mysql_fetch_row($result);
		else
			$page_no = 0;
		
		return array($page_no, $anchor);
	}
	
	function set_default_link($link)
	{
		list($page_no, $anchor) = $this->_split_link($link);

		mysql_query(
			'UPDATE book ' .
			'SET page_no = ' . $page_no . ', ' .
				'anchor = "' . mysql_escape_string($anchor) . '" ' .
			'WHERE id = ' . $this->id 
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
	}
	
	function add_toc_entry($title, $link, $parent_no = 0)
	{
		list($page_no, $anchor) = $this->_split_link($link);

		$this->last_toc_entry_no += 1;
		mysql_query(
			'INSERT ' .
			'INTO toc_entry ' .
			'(book_id, parent_no, no, title, page_no, anchor)' .
			'VALUES (' . 
				$this->id . ', ' .
				$parent_no . ', ' .
				$this->last_toc_entry_no . ', ' .
				'"' . mysql_escape_string($title) . '", ' .
				$page_no . ', ' .
				'"' . mysql_escape_string($anchor) . '")'
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
		
		return $this->last_toc_entry_no;
	}
	
	function add_index_entry($term, &$links)
	{
		foreach($links as $link)
		{
			list($path, $anchor) = $this->__split_link($link);
			
			mysql_query(
				'INSERT ' .
				'INTO temp_index_entry ' .
				'(term, path, anchor) ' .
				'VALUES (' . 
					'"' . mysql_escape_string($term) . '", ' .
					'"' . mysql_escape_string($path) . '", ' .
					'"' . mysql_escape_string($anchor) . '"' .
				')'
			) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
		}
	}
	
	function commit()
	{
		echo "  commiting index\n";
		ob_flush();
		flush();	
		
		mysql_query(
			"ALTER 
			TABLE temp_index_entry
			ADD INDEX term (term(7))"
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
		
		mysql_query(
			"SET @index_no := 0"
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error() . "\n");

		mysql_query(
			"INSERT " .
			"INTO index_entry (book_id, no, term) " .
			"SELECT $this->id, @index_no := (@index_no + 1), temp_index_entry.term " .
			"FROM temp_index_entry " .
			"GROUP BY temp_index_entry.term"
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error() . "\n");

		mysql_query(
			"INSERT " .
			"INTO index_link (book_id, no, page_no, anchor) " .
			"SELECT $this->id, index_entry.no, page.no, anchor " .
			"FROM index_entry " .
				"LEFT JOIN temp_index_entry USING(term) " .
				"LEFT JOIN page ON page.book_id = $this->id AND page.path = temp_index_entry.path " .
			"WHERE index_entry.book_id = $this->id"
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error() . "\n");
		
		mysql_query(
			"DROP /*!40000 TEMPORARY */ TABLE temp_index_entry" 
		) or die(__FILE__ . ':' . __LINE__ . ':' . mysql_error());
		
		echo "  commencing fulltext index\n";
		$this->index_fulltext();
		
		$this->committed = TRUE;
	}
}

?>

<?php

require_once 'inc/config.inc.php';
require_once 'lib/util.lib.php';
require_once 'lib/tar.class.php';

class XmlParser
{
    var $parser;

    function XmlParser($encoding = 'UTF-8')
    {
        $this->parser = & xml_parser_create();

        xml_set_object($this->parser, $this);
        
        xml_set_element_handler($this->parser, '_start_element', '_end_element');
        xml_set_character_data_handler($this->parser, '_cdata');
        
        xml_parser_set_option($this->parser, XML_OPTION_CASE_FOLDING, 0);
        xml_parser_set_option($this->parser, XML_OPTION_TARGET_ENCODING, $encoding);
    }

    function parse_string(&$string)
    {
		xml_parse($this->parser, $string);
    }

    function parse_file($filename)
    {
    	$handle = fopen($filename, 'rt');
		while(!feof($handle))
		{
			$data = fread($handle, 8192);
			xml_parse($this->parser, $data, FALSE);
		}
		xml_parse($this->parser, $data, TRUE);
		fclose($handle);
    }

    function _start_element(&$parser, $tag, &$attribs)
    {
    	$this->start_element($tag, $attribs);
    }

    function _cdata(&$parser, $cdata)
    {
    	$this->cdata($cdata);
    }
    
    function _end_element(&$parser, $tag)
    {
    	$this->end_element($tag);
    }

    function start_element($tag, &$attribs) {}

    function cdata($cdata) {}

    function end_element($tag) {}
}

class DevhelpSpecParser extends XmlParser
{
    var $book;
    
    var $toc_parent_no;
    var $toc_parent_no_stack;

    function DevhelpSpecParser(&$book, $encoding = 'UTF-8')
    {
    	$this->XmlParser($encoding);
    	
    	$this->book = &$book;

		$this->toc_parent_no = 0;
		$this->toc_parent_no_stack = array();
    }

    function start_element($tag, &$attribs)
    {
    	switch($tag)
    	{
    		case 'book':
    		
    			// TODO: handle 'base' attribute
    		
    			if(isset($attribs['title']))
    				$this->book->set_title($attribs['title']);
    			
    			if(isset($attribs['link']))
    				$this->book->set_default_link($attribs['link']);

    			if(isset($attribs['name']))
    				$this->book->set_metadata('name', $attribs['name']);
    				
    			if(isset($attribs['version']))
    				$this->book->set_metadata('version', $attribs['version']);
    			
    			break;
    		
    		case 'chapter':
    		case 'sub':
    			$title = $attribs['name'];
    			$link = $attribs['link'];

      			array_push($this->toc_parent_no_stack, $this->toc_parent_no);
    			
    			$this->toc_parent_no = $this->book->add_toc_entry($title, $link, $this->toc_parent_no);
      			
    			break;
    		
    		case 'function':
    			$term = $attribs['name'];
    			$links = array($attribs['link']);
    			
    			$this->book->add_index_entry($term, $links);
    			
    			break;
    	}
    }

    function end_element($tag)
    {
    	switch($tag)
    	{
    		case 'chapter':
    		case 'sub':
    			$this->toc_parent_no = array_pop($this->toc_parent_no_stack);
    			break;    		
    	}
    }
}

class DevhelpReader
{
	function DevhelpReader($filename)
	{
		$this->tar = & new tar();

		// FIXME: tar file is uncompressed to memory. 
		if(!$this->tar->openTar($filename, TRUE))
			die ($filename . ': Could not open tar file');
	}
	
	function read(&$book)
	{
		// add pages
		$pages = $this->list_pages();
		foreach($pages as $path)
		{
			$content = & $this->get_page($path);
			$book->add_page($path, $content);
		}
		
		// parse spec
		if(!($information = & $this->tar->getFile('book.devhelp')))
			die('book.devhelp: file not found');
		$file = $information['file'];
		global $internal_encoding;
		$parser = & new DevhelpSpecParser($book, $internal_encoding);
		$parser->parse_string($file);
		
		// commit changes
		$book->commit();
	}
	
	function list_pages()
	{
		$basedir = '/book/';
		$pages = array();
		foreach($this->tar->files as $id => $information)
		{
			$path = $information['directory'] . '/' . $information['name'];
			if(substr($path, 0, strlen($basedir)) == $basedir)
				$pages[] = substr($path, strlen($basedir)); 
		}
		return $pages;
	}
	
	function get_page($path)
	{
		$information = & $this->tar->getFile('book/' . $path);
		return $information['file'];
	}
}

?>

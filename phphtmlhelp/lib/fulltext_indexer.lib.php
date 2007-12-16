<?php

require_once 'lib/mbstring.lib.php';
require_once 'lib/mimetypes.lib.php';

// Extracts title and lexemes from documents
class Fulltext_Indexer
{
	var $index;
	var $tokenizer;

	function Fulltext_Indexer(& $index)
	{
		$this->index = & $index;
		$this->tokenizer = & $index->tokenizer;
	}

	function set_title($title)
	{
		$title = $this->tokenizer->normalize($title);
		$this->index->handle_item_title($title);
	}

	function feed_body($body)
	{
		$lexemes = & $this->tokenizer->tokenize($body);
		$lexemes = & $this->tokenizer->filter($lexemes);		
		$this->index->handle_item_lexemes($lexemes);
	}

	function feed(&$content) {}
}

// Indexes plain-text documents
class Fulltext_TextIndexer extends Fulltext_Indexer
{
	function feed(&$content)
	{
		$this->feed_body($content);
	}
}

// Indexes HTML documents
class Fulltext_HtmlIndexer extends Fulltext_Indexer
{
	function feed(&$content)
	{
		$encoding = $this->extract_encoding($content);

		$title = $this->extract_title($content, $encoding);
		if($title)
			$this->set_title($title);

		/*
		$body_parts = & $this->extract_body_parts($content, $encoding);
		foreach($body_parts as $body_part)
			$this->feed_body($body_part);
		*/
		$body = $this->extract_body($content, $encoding);
		$this->feed_body($body);		
	}
	
	function decode_html($html, $encoding = 'ISO-8859-1')
	{
		$html = mb_convert_encoding($html, $this->index->encoding, $encoding);
		return html_entity_decode($html, ENT_QUOTES, $this->index->encoding);
	}	

	function extract_encoding(&$html, $default_encoding='ISO-8859-1')
	{
		// extract encoding from XML header
		if(preg_match(
				'/^<\?xml' . 
					// other attributes
					'(?:\s+[-a-zA-Z0-9._:]+\s*=\s*(?:"[^"]*"|\'[^\']*\'))*?' . 
					// encoding attribute
					'\s+encoding\s*=\s*(?:"([^"]*)"|\'([^\']*)\')' .
					// other attributes
					'(?:\s+[-a-zA-Z0-9._:]+\s*=\s*(?:"[^"]*"|\'[^\']*\'))*?' . 
				'\s*\?>/', $html, $matches))
		{
			$encoding = $matches[1] . $matches[2];
			return trim($encoding);
		}
		// extract encoding from HTML META declaration, per
		// http://www.w3.org/TR/html401/charset.html#h-5.2.2
		elseif(preg_match(
				'/<META' .
					// other attributes
					'(?:\s+[-a-zA-Z0-9._:]+\s*=\s*(?:[-a-zA-Z0-9._:]+|"[^"]*"|\'[^\']*\'))*?' . 
					// http-equiv attribute
					'\s+http-equiv\s*=\s*(?:Content-Type|"Content-Type"|\'Content-Type\')' .
					// other attributes
					'(?:\s+[-a-zA-Z0-9._:]+\s*=\s*(?:[-a-zA-Z0-9._:]+|"[^"]*"|\'[^\']*\'))*?' .
					// content attribute
					'\s+content\s*=\s*(?:([-a-zA-Z0-9._:]+)|"([^"]*)"|\'([^\']*)\')' .
					// other attributes
					'(?:\s+[-a-zA-Z0-9._:]+\s*=\s*(?:[-a-zA-Z0-9._:]+|"[^"]*"|\'[^\']*\'))*?' .
				'\s*>/i', $html, $matches))
		{
			$http_equiv = html_entity_decode($matches[1] . $matches[2] . $matches[3]);
			if(preg_match('/^text\/html;\s*charset=(?:([-a-zA-Z0-9._:]+)|"([^"]*)"|\'([^\']*)\')/', $http_equiv, $matches))
			{
				$encoding = $matches[1] . $matches[2] . $matches[3];
				return $encoding;
			}
		}
		return $default_encoding;
	}

	function extract_title(&$html, $encoding=NULL)
	{
		if(!isset($encoding))
			$encoding = $this->extract_encoding($html);

		if(preg_match(
				// body start tag
				'/<TITLE(?:\s+[^>]*)?>' . 
				// body text
				'(.*?)' . 
				// body end tag
				'<\/TITLE\s*>/is', $html, $matches))
			return $this->decode_html($matches[1], $encoding);
		else
			return NULL;
	}

	function extract_body(&$html, $encoding=NULL)
	{
		if(!isset($encoding))
			$encoding = $this->extract_encoding($html);

		$body = preg_replace(
			array(
				// everything till body start tag
				'/^.*<BODY(?:\s+[^>]*)?>/is', 
				// everything after body end tag
				'/<\/BODY\s*>.*$/is',
				// any tag
				'/<[^>]*>/'),
			array(
				'',
				'',
				' '),
			$html
		);
		return $this->decode_html($body, $encoding); 
	}
}

// Fulltext_Indexer Factory Method
function Fulltext_indexer_factory($path, &$index)
{
	$content_type = guess_type($path);
	if($content_type == "text/plain")
		return new Fulltext_TextIndexer($index);
	elseif($content_type == "text/html")
		return new Fulltext_HtmlIndexer($index);
	return NULL;
}
?>

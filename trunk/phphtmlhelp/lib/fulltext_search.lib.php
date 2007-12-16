<?php

class Fulltext_SearchResult
{
	// TODO: It may be possible to write another version of this class which 
	// compiles SQL statements, resorting to subselects or temporary tables...

	var $entries;

	function Fulltext_SearchResult(&$entries) 
	{
		$this->entries = &$entries;
	}

	function union(&$other) 
	{
		// FIXME: implement this
	}

	function intersection(&$other)
	{
		$entries = array();
		foreach($this->entries as $item => $score)
			if(isset($other->entries[$item]))
				$entries[$item] = $score * $other->entries[$item];
		return new Fulltext_SearchResult($entries);
	}

	function subtraction(&$other)
	{
		// FIXME: implement this
	}

	function enumerate()
	{
		arsort($this->entries, SORT_NUMERIC);
		return $this->entries;
	}
}

class Fulltext_SearchNode
{
	// Should be overriden by derived classes
	function apply(&$searchable)
	{
		// TODO: include score
		return array();
	}
}

class Fulltext_TermSearchNode extends Fulltext_SearchNode
{
	var $term;

	function Fulltext_TermSearchNode($term)
	{
		$this->term = $term;
	}

	function apply(&$searchable)
	{
		return $searchable->search_lexeme($this->term);
	}
}

class Fulltext_AndSearchNode extends Fulltext_SearchNode
{
	var $left_node;
	var $right_node;

	function Fulltext_AndSearchNode(&$left_node, &$right_node)
	{
		$this->left_node = &$left_node;
		$this->right_node = &$right_node;
	}

	function apply(&$searchable)
	{
		$lresult = & $this->left_node->apply($searchable);
		$rresult = & $this->right_node->apply($searchable);
		return $lresult->intersection($rresult);
	}
}

// parse a search query string
function Fulltext_Search_parse($query, &$tokenizer)
{
	// TODO: implement more complex searches
	$lexemes = & $tokenizer->tokenize($query);
	$lexemes = & $tokenizer->filter($lexemes);

	$search = & new Fulltext_TermSearchNode($lexemes[0]);
	unset($lexemes[0]);
	foreach($lexemes as $lexeme)
		$search = & new Fulltext_AndSearchNode($search, new Fulltext_TermSearchNode($lexeme));
	return $search;
}

?>

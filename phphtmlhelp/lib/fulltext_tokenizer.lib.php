<?php

// Stop words
$stop_words = array();
# From http://en.wikipedia.org/wiki/Stop_words
$handle = fopen("misc/stop_words.txt", "rt");
while(!feof($handle))
	 if($word = trim(fgets($handle, 4096)))
	 	$stop_words[$word] = TRUE;
fclose($handle);

// Based on Lucene's standard tokenizer
// http://svn.apache.org/repos/asf/lucene/java/trunk/src/java/org/apache/lucene/analysis/standard/StandardTokenizer.jj

// A tokenizer extracts and filters tokens
class Fulltext_Tokenizer
{
	// Pattern modifiers 
	var $modifiers = '';
	
	// Base character classes
	var $letter = 'a-zA-Z';
	var $digit = '0-9';
	var $cjk = '';
	var $space = '\s';
	
	// Uppercase/lowercase letters
	var $upper = '';
	var $lower = '';
	
	// composite token regular expression
	var $token_pattern;
	
	function Fulltext_Tokenizer()
	{
		$letter = $this->letter;
		$digit = $this->digit;
		$cjk = $this->cjk;
			
		// NOTE: order *does* matter: first match is chosen
		// NOTE: branches '|' should be inside subpatterns '(?: ... )'
		$tokens = array(
			// acronyms
			"[$letter]\.(?:[$letter]\.)+",
		
			// email addresses (according to http://www.developer.com/lang/php/article.php/3290141)
			'[_a-zA-Z0-9-]+(?:\.[_a-zA-Z0-9-]+)*@[_a-zA-Z0-9-]+(?:\.[_a-zA-Z0-9-]+)*\.[a-zA-Z]{2,4}',
		
			// company names
			"[$letter]+[&@][$letter]+",
		
			// internal apostrophes
			"[$letter]+(?:\'[$letter]+)+",
		
			// floating point numbers
			'(?:\d+|\d+[.,]\d*|\d*[.,]\d+)[eE][-+]?\d+',
		
			// versions and ip numbers
			'[a-zA-Z]*\d+[a-zA-Z]*(?:\.[a-zA-Z]*\d+[a-zA-Z]*)+',
		
			// dates
			'\d+-\d+-\d+|\d+\/\d+\/\d+',
		
			// decimal numbers
			'\d*[.,]\d+',
		
			// paths?
		
			// identifiers
			'[_a-zA-Z][_a-zA-Z0-9]+',
		
			// basic word: a sequence of letters and digits
			"[$letter$digit]{2,}",
		);
		
		if($cjk)
			$tokens[] = "[$cjk]";
		
		$this->token_pattern = '/' . implode('|',  $tokens) . '/' . $this->modifiers;
		
		global $stop_words;
		$this->stop_word_tr = array();
		foreach($stop_words as $stop_word => $flag)
			$this->stop_word_tr[" " . $stop_word . " "] = "";
	}
	
	// find tokens in a string
	function tokenize($string)
	{
		preg_match_all($this->token_pattern, $string, $matches, PREG_PATTERN_ORDER);
		$tokens = & $matches[0];
		return $tokens;
	}

	function tolower($string)
	{
		return strtr($string, $this->upper, $this->lower);
	}

	function filter(&$tokens)
	{
		// glue tokens together to speed processing
		$string = " " . implode("  ", $tokens) . " ";
		
		// change to lower case
		$string = $this->tolower($string);
		
		// eliminate stopwords
		$string = strtr($string, $this->stop_word_tr);

		// breaks tokens again
		return explode("  ", substr($string, 1, strlen($string) - 2));
	}
	
	// split a tring in whitespace
	function split($string)
	{
		return preg_split('/[' . $this->space . ']+/' . $this->modifiers, $string, -1, PREG_SPLIT_NO_EMPTY);
	}

	// normalize whitespace
	function normalize($string)
	{
		return implode(' ', $this->split($string));
	}
}

class Fulltext_Ascii_Tokenizer extends Fulltext_Tokenizer
{
	var $modifiers = '';
	
	var $letter = "A-Za-z";
	var $digit = "0-9";
	var $cjk = "";
	var $space = "\x09-\x0D\x20";
	
	var $upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	var $lower = "abcdefghijklmnopqrstuvwxyz";
}

class Fulltext_Iso88591_Tokenizer extends Fulltext_Ascii_Tokenizer
{
	var $letter = "A-Za-z\xC0-\xD6\xD8-\xF6\xF8-\xFF";
	var $digit = "0-9";
	var $cjk = "";
	var $space = "\x09-\x0D\x20\x85\xA0";

	var $upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD8\xD9\xDA\xDB\xDC\xDD\xDE";
	var $lower = "abcdefghijklmnopqrstuvwxyz\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF\xF0\xF1\xF2\xF3\xF4\xF5\xF6\xF8\xF9\xFA\xFB\xFC\xFD\xFE";
}

// FIXME: complete support ISO-8859-15
class Fulltext_Iso885915_Tokenizer extends Fulltext_Iso88591_Tokenizer
{
	var $letter = "A-Za-z\xA6\xA8\xAA\xB4\xB5\xB8\xBA\xBC-\xBE\xC0-\xD6\xD8-\xF6\xF8-\xFF";
	
	var $upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ\xA6\xB4\xBC\xBE\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD8\xD9\xDA\xDB\xDC\xDD\xDE";
	var $lower = "abcdefghijklmnopqrstuvwxyz\xA8\xB8\xBD\xFF\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF\xF0\xF1\xF2\xF3\xF4\xF5\xF6\xF8\xF9\xFA\xFB\xFC\xFD\xFE";
}

class Fulltext_Utf8_Tokenizer extends Fulltext_Ascii_Tokenizer
{
	var $modifiers = 'u';
	
	var $letter = 'A-Za-z\x{00C0}-\x{00D6}\x{00D8}-\x{00F6}\x{00F8}-\x{00FF}\x{0100}-\x{1FFF}';
	var $digit = '0-9\x{0660}-\x{0669}\x{06F0}-\x{06F9}\x{0966}-\x{096F}\x{09E6}-\x{09EF}\x{0A66}-\x{0A6F}\x{0AE6}-\x{0AEF}\x{0B66}-\x{0B6F}\x{0BE7}-\x{0BEF}\x{0C66}-\x{0C6F}\x{0CE6}-\x{0CEF}\x{0D66}-\x{0D6F}\x{0E50}-\x{0E59}\x{0ED0}-\x{0ED9}\x{1040}-\x{1049}';
	var $cjk = '\x{3040}-\x{318F}\x{3300}-\x{337F}\x{3400}-\x{3D2D}\x{4E00}-\x{9FFF}\x{F900}-\x{FAFF}';
	// based on http://www.unicode.org/Public/4.1.0/ucd/PropList.txt:
	var $space = '\x{0009}-\x{000D}\x{0020}\x{0085}\x{00A0}\x{1680}\x{180E}\x{2000}-\x{200A}\x{2028}\x{2029}\x{202F}\x{205F}\x{3000}';	

	function tolower($string)
	{
		return mb_strtolower($string, 'UTF-8');
	}
}

$_tokenizers = array(
	'ASCII' => new Fulltext_Ascii_Tokenizer(),
	'ISO-8859-1' => new Fulltext_Iso88591_Tokenizer(),
	'ISO-8859-15' => new Fulltext_Iso885915_Tokenizer(),
	'UTF-8' => new Fulltext_Utf8_Tokenizer(),
);

function Fulltext_tokenizer_factory($encoding)
{
	global $_tokenizers;

	if(!isset($_tokenizers[$encoding]))
		$encoding = 'ASCII';
	
	return $_tokenizers[$encoding];
}

?>

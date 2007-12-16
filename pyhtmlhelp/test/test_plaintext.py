#!/usr/bin/env python


import unittest

from htmlhelp.util.plaintext import *


class PlaintextTestCase(unittest.TestCase):
	
	def testNormalizeSpace(self):
		for string, result in [
				('', ''),
				('  ', ''),
				('  a sentence', 'a sentence'),
				(' a   sentence ', 'a sentence'),
				('a  sentence', 'a sentence')]:
			self.failUnlessEqual(normalize_space(string), result)
			
	def testHtmlEntityDecode(self):
		for string, encoding, result in [
				(' &lt; cheap &amp; easy! &gt; ', 'iso-8859-1', ' < cheap & easy! > '),
				('&#xE1;', 'utf-8', u'\xe1')]:
			self.failUnlessEqual(html_entity_decode(string, encoding), result)
	
	def testExtractHtml(self):
		for string, title, body in [
				('<html><head><title id="123">The title</title></head><body class="test"></body></html>',
					'The title', '')]:
			self.failUnlessEqual(extract_html(string), (title, body))
	
	def testGuessType(self):
		for path, mime_type in [
				('dir/subdir/name.htm', 'text/html'),
				('dir/subdir/name.html', 'text/html')]:
			self.failUnlessEqual(guess_type(path), mime_type)

	def testWordCount(self):
		for string, result in [
				('one two three two three three', {'one': 1, 'two': 2, 'three': 3})]:
			self.failUnlessEqual(word_count(string), result)
	
	def testFulltextIndex(self):
		for before, path, string, after in [
				(
					{'worda': {'pagea': 1}}, 
					'pageb', 'worda wordb wordb', 
					{'worda': {'pagea':1, 'pageb':1}, 'wordb': {'pageb': 2}}
				)]:
			index = before
			fulltext_index(index, path, string)
			self.failUnlessEqual(index, after)


if __name__ == '__main__':
	unittest.main()

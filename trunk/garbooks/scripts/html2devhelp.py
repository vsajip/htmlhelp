#!/usr/bin/env python


import re
import sys
import HTMLParser
import htmlentitydefs

class XmlWriter:
	"""Writes a XML document."""

	def __init__(self, fp, encoding = 'utf-8', indent = False):
		self.fp = fp
		self.encoding = encoding
		self.indent = indent
		self.level = 0
	
	def start_doc(self):
		self.fp.write('<?xml version="1.0" encoding="%s"?>' % self.encoding)
	
	def end_doc(self):
		pass
		
	def start_tag(self, tag, **attributes):
		if self.indent:
			self.fp.write('\t'*self.level)
		self.fp.write('<' + tag)
		for name, value in attributes.iteritems():
			self.fp.write(' ' + name + '="' + self.escape(value) + '"')
		self.fp.write('>')
		if self.indent:
			self.fp.write('\n')
		self.level += 1

	def end_tag(self, tag):
		self.level -= 1
		if self.indent:
			self.fp.write('\t'*self.level)
		self.fp.write('</' + tag + '>')
		if self.indent:
			self.fp.write('\n')
	
	def tag(self, tag, **attributes):
		if self.indent:
			self.fp.write('\t'*self.level)
		self.fp.write('<' + tag)
		for name, value in attributes.iteritems():
			self.fp.write(' ' + name + '="' + self.escape(value) + '"')
		self.fp.write('/>')
		if self.indent:
			self.fp.write('\n')

	def escape(self, s):
		"""Helper to add special character quoting."""
		
		if s is None:
			return ''
		
		s = s.replace("&", "&amp;") # Must be first
	
		if isinstance(s, unicode):
			s = s.encode(self.encoding, 'xmlcharrefreplace')
	
		s = s.replace("<", "&lt;")
		s = s.replace(">", "&gt;")
		s = s.replace("'", "&apos;")
		s = s.replace('"', "&quot;")
	
		return s

	def binary(self, s):
		self.fp.write(base64.encodestring(s))


class DevhelpWriter(XmlWriter):
	"""Writes a DevHelp spec file."""

	def start_book(self, title, link, metadata):
		attrs = {}
		if 'name' in metadata:
			attrs['version'] = metadata['version']
		if 'version' in metadata:
			attrs['version'] = metadata['version']
		if 'author' in metadata:
			attrs['author'] = metadata['author']
		self.start_tag('book', name=name, title=title, link=contents.link)

	def start_chapters(self):
		self.start_tag('chapters')

	def start_chapter(self, name, link):
		self.start_tag('sub', name=name, link=link)

	def end_chapter(self):
		self.end_tag('sub')

	def end_chapters(self):
		self.end_tag('chapters')

	def start_functions(self):
		self.start_tag('functions')

	def function(self, term, link):
		self.tag('function', name=term, link=link)
	
	def end_functions(self):
		self.end_tag('functions')

	def end_book(self):
		self.end_tag('book')


def normalize_space(s):
	"""Normalize whitespace."""

	return ' '.join(s.split())



class BaseParser(HTMLParser.HTMLParser):

	def __init__(self, writer):
		HTMLParser.HTMLParser.__init__(self)
		self.writer = writer
		
	def handle_starttag(self, name, attributes):
		method = 'start_' + name
		if hasattr(self, method):
			_attributes = {}
			for key, value in attributes:
				_attributes[key.encode()] = value
			apply(getattr(self, method), (), _attributes)
	
	def handle_endtag(self, name):
		method = 'end_' + name
		if hasattr(self, method):
			apply(getattr(self, method))
	
	def handle_charref(self, name):
			self.handle_data(unichr(int(name)))

	def handle_entityref(self, name):
			self.handle_data(unichr(htmlentitydefs.name2codepoint[name]))

	def parse(self, fp):
		self.feed(fp.read())
		self.close()
	

class TocParser(BaseParser):

	level = 0
	in_li = False
	in_a = False
	name = None
	link = None

	def start_ul(self, **dummy):
		if not self.level:
			self.writer.start_chapters()
		self.level += 1
		self.in_li = False
	
	def end_ul(self):
		if self.in_li:
			self._end_li()
		self.level -= 1
		if not self.level:
			self.writer.end_chapters()
		self.in_li = True

	start_ol = start_ul
	end_ol = end_ul

	def start_li(self, **dummy):
		if self.in_li:
			self._end_li()
		self.in_li = True

	def _end_li(self):
		self.writer.end_chapter()	
		self.in_li = False

	def start_a(self, href=None, **dummy):
		if self.in_li:
			self.in_a = True
			self.name = ''
			self.link = href
		
	def end_a(self):
		if self.in_a:
			self.name = normalize_space(self.name)
			self.writer.start_chapter(self.name, self.link)	
			self.in_a = False
	
	def handle_data(self, data):
		if self.in_a:
			self.name += data
	

class AIndexParser(BaseParser):

	in_a = False

	def start_a(self, href=None, **dummy):
		if href is not None:
			self.link = href
			self.in_a = True
			self.name = ''
		
	def end_a(self):
		self.in_a = False
		name = normalize_space(self.name)
		self.writer.function(name, self.link)
	
	def handle_data(self, data):
		if self.in_a:
			self.name += data

class UlIndexParser(BaseParser):

	in_li = False
	in_a = False

	def start_ul(self, **dummy):
		pass
		#self.writer.start_functions()

	def end_ul(self):
		pass
		#self.writer.end_functions()

	def start_li(self, **dummy):
		self.in_li = True
		self.name = ''

	def end_dt(self):
		self.in_li = False

	def start_a(self, href=None, **dummy):
		if self.in_li and href is not None:
			name = normalize_space(self.name)
			link = href
			self.writer.function(name, link)
			self.in_a = True
		
	def end_a(self):
		self.in_a = False
	
	def handle_data(self, data):
		if not self.in_a:
			if self.in_li:
				self.name += data
	

class DtIndexParser(BaseParser):

	in_dt = False
	in_dd = False
	in_a = False

	def start_dl(self, **dummy):
		pass
		#self.writer.start_functions()

	def end_dl(self):
		pass
		#self.writer.end_functions()

	def start_dt(self, **dummy):
		self.in_dt = True
		self.dt = ''
		self.dd = None

	def end_dt(self):
		self.in_dt = False

	def start_dd(self, **dummy):
		self.in_dd = True
		self.dd = ''

	def end_dd(self):
		self.in_dd = False

	def start_a(self, href=None, **dummy):
		if (self.in_dt or self.in_dd) and href is not None:
			name = self.dt
			if self.in_dd:
				name += ', '
				name += self.dd
			name = normalize_space(name)
			link = href
			self.writer.function(name, link)
			self.in_a = True
		
	def end_a(self):
		self.in_a = False
	
	def handle_data(self, data):
		if not self.in_a:
			if self.in_dt:
				self.dt += data
			if self.in_dd:
				self.dd += data


def main():
	arg = sys.argv[1]
	writer = DevhelpWriter(sys.stdout, indent=True)
	factories = {
		'toc': TocParser,
		'aidx': AIndexParser,
		'ulidx': UlIndexParser,
		'dtidx': DtIndexParser,
	}
	factory = factories[arg]
	parser = factory(writer)
	parser.parse(sys.stdin)

if __name__ == '__main__':
	main()

# %s/">\n\t\+<\/sub>/"\/>/

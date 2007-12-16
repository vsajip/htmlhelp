'''Utilities for dealing with XML files.'''


import base64
import xml.parsers.expat


class XmlParser:
	"""Base XML document parser."""
	
	def handle_element_start(self, name, attributes):
		method = 'start_' + name
		if hasattr(self, method):
			_attributes = {}
			for key, value in attributes.iteritems():
				_attributes[key.encode()] = value
			apply(getattr(self, method), (), _attributes)
	
	def handle_element_end(self, name):
		method = 'end_' + name
		if hasattr(self, method):
			apply(getattr(self, method))
	
	def parse(self, fp):
		parser = xml.parsers.expat.ParserCreate()
		parser.StartElementHandler = self.handle_element_start
		parser.EndElementHandler = self.handle_element_end
		parser.ParseFile(fp)


class XmlFormatter:
	"""Formats a XML document."""

	def __init__(self, fp, encoding = 'utf-8'):
		self.fp = fp
		self.encoding = encoding
		
		self.fp.write('<?xml version="1.0" encoding="%s"?>' % self.encoding)
	
	def start_tag(self, tag, **attributes):
		self.fp.write('<' + tag)
		for name, value in attributes.iteritems():
			self.fp.write(' ' + name + '="' + self.escape(value) + '"')
		self.fp.write('>')

	def end_tag(self, tag):
		self.fp.write('</' + tag + '>')
	
	def tag(self, tag, **attributes):
		self.fp.write('<' + tag)
		for name, value in attributes.iteritems():
			self.fp.write(' ' + name + '="' + self.escape(value) + '"')
		self.fp.write('/>')

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


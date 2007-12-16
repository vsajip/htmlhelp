"""XML-based self-contained format for books."""


import sys
import gzip

from htmlhelp.book import Book
from htmlhelp.format import Format
from htmlhelp.util.xml_ import XmlFormatter


class XmlBookFormatter(XmlFormatter):
	
	def book(self, book):
		self.start_tag('book', name=book.name, title=book.title, link=book.default_link)
		self.contents(book.contents)
		self.index(book.index)
		self.metadata(book.metadata)
		self.archive(book.archive)
		self.end_tag('book')
		
	def contents(self, contents):
		self.start_tag('contents')
		self.contents_entries(contents)
		self.end_tag('contents')	
		
	def contents_entries(self, entry):
		for subentry in entry:
			# TODO: use single tags when possible
			self.start_tag('contents_entry', name = subentry.name, link = subentry.link)
			self.contents_entries(subentry)
			self.end_tag('contents_entry')	
	
	def index(self, index):
		self.start_tag('index')
		for entry in index:
			for	link in entry.links:
				self.tag('index_entry', name=entry.name, link=link)
		self.end_tag('index')	
	
	def metadata(self, metadata):
		for name, value in metadata.iteritems():
			pass
		
	def archive(self, archive):
		self.start_tag('pages')
		for path in archive:
			self.start_tag('page', path=path)
			content = archive[path].read()
			self.binary(content)
			self.end_tag('page')
		self.end_tag('pages')


class XmlFormat(Format):
	
	def __init__(self):
		Format.__init__(self, 'xml')
		
	def write(self, book, path, **options):
		# TODO: handle gziped and bziped xml files too
		if not path.endswith('.xml'):
			raise NotImplementedError
		formatter = XmlBookFormatter(file(path, 'wt'))
		formatter.book(book)

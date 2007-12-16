"""DevHelp Books.

See http://www.imendio.com/projects/devhelp/ for more information about DevHelp.
"""


import os
import os.path
import urlparse
import tarfile
import time

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

from htmlhelp.archive.dir import DirArchive
from htmlhelp.archive.tar import TarArchive
from htmlhelp.archive.filter import FilterArchive
from htmlhelp.book import Book, Contents, ContentsEntry, Index, IndexEntry
from htmlhelp.util.xml_ import XmlParser, XmlFormatter
from htmlhelp.format import Format


#######################################################################
# DevHelp XML spec parsing/formatting
#
# For format description see:
# - http://cvs.gnome.org/lxr/source/devhelp/dtd/devhelp-1.dtd
# - http://cvs.gnome.org/lxr/source/devhelp/README


class SpecParser(XmlParser):
	"""DevHelp spec file parser."""

	def __init__(self):
		self.contents = Contents()
		self.contents_stack = [self.contents]
		
		self.index = Index()

		self.metadata = {}

		self.base = None
		
	def translate_link(self, link):
		if self.base is None:
			return link
		else:
			return urlparse.urljoin(self.base, link)
			
	def start_book(self, name, title, link, base = None, author = None, version = None, **dummy):
		assert len(self.contents_stack) == 1

		if base is not None:	# Must be first
			self.base = base
		
		self.contents.name = title
		self.contents.link = self.translate_link(link)

		# Metadata
		self.metadata['name'] = name
		if version is not None:
			self.metadata['version'] = version
		if author is not None:
			self.metadata['author'] = author
	
	def end_book(self):
		assert len(self.contents_stack) == 1
	
	def start_chapter(self, name, link, **dummy):
		assert len(self.contents_stack) > 0

		entry = ContentsEntry(name, self.translate_link(link))
		self.contents_stack[-1].append(entry)
		self.contents_stack.append(entry)
		
	def end_chapter(self):
		assert len(self.contents_stack) > 1
		
		self.contents_stack.pop()

	start_sub = start_chapter

	end_sub = end_chapter
	
	def start_function(self, name, link, **dummy):
		entry = IndexEntry(name, self.translate_link(link))
		self.index.append(entry)


class SpecFormatter(XmlFormatter):

	def book(self, book, name = None):
		if name is None:
			if book.name is None:
				raise ValueError, 'Required book name not specified.'
			name = book.name

		attrs = {}
		if 'version' in book.metadata:
			attrs['version'] = book.metadata['version']
		if 'author' in book.metadata:
			attrs['author'] = book.metadata['author']
		self.start_tag('book', name=name, title=book.contents.name, link=book.contents.link)
		self.chapters(book.contents)
		self.functions(book.index)
		self.end_tag('book')

	def chapters(self, contents):
		self.start_tag('chapters')
		self.chapter(contents)
		self.end_tag('chapters')

	def chapter(self, parent):
		for child in parent:
			if len(child):
				self.start_tag('sub', name=child.name, link=child.link)
				self.chapter(child)
				self.end_tag('sub')
			else:
				self.tag('sub', name=child.name, link=child.link)

	def functions(self, index):
		self.start_tag('functions')
		for entry in index:
			self.function(entry)
		self.end_tag('functions')

	def function(self, entry):
		name = entry.name
		for link in entry.links:
			self.tag('function', name=name, link=link)


#######################################################################
# Archive filters


class DirDevhelpFilterArchive(FilterArchive):
	"""Hides the spec file from the client."""
	
	def filter(self, path):
		if not path.endswith('.devhelp'):
			return path
		else:
			return None


class TgzDevhelpFilterArchive(FilterArchive):
	""""HTML pages in DevHelp tgz books  are stored in the 'book' subdirectory.
	This filter hides that from the client."""

	def filter(self, path):
		if path.startswith('book/'):
			return path[5:]
		else:
			return None

	def translate(self, path):
		return 'book/' + path


#######################################################################
# Format


class DevhelpFormat(Format):
	
	def __init__(self):
		Format.__init__(self, 'devhelp')
		
		self.path = []

		if 'HOME' in os.environ:
			self.path.append(os.path.join(os.environ['HOME'], '.devhelp', 'books'))
		
		self.path.append('/usr/share/gtk-doc/html')
		self.path.append('/usr/local/share/gtk-doc/html')

	def read_spec(self, path):
		"""Read a DevHelp book on a plain directory."""
	
		basedir, spec = os.path.split(os.path.abspath(path))
		
		name = os.path.splitext(spec)[0]
	
		archive = DirArchive(basedir)
	
		parser = SpecParser()
		parser.parse(file(path, 'rt'))
	
		book = Book(
				name,
				DirDevhelpFilterArchive(archive),
				parser.contents,
				parser.index,
				parser.metadata)
	
		return book
	
	def read_tgz(self, path):
		"""A DevHelp book in a gzip'ed tarball."""
	
		name = os.path.splitext(os.path.basename(path))[0]
	
		archive = TarArchive(path)
	
		parser = SpecParser()
		parser.parse(archive['book.devhelp'])
	
		book = Book(
				name,
				TgzDevhelpFilterArchive(archive),
				parser.contents,
				parser.index,
				parser.metadata)
	
		return book

	def read(self, path, **options):
		"""Attempt to open a DevHelp book from the given path."""
		
		root, ext = os.path.splitext(path)
		if ext == '.devhelp':
			return self.read_spec(path)
		elif ext == '.tgz':
			return self.read_tgz(path)
		else:
			raise ValueError, 'unknown DevHelp book extension \'%s\'' % ext

	def _addfile(self, tar, name, fp):
		tarinfo = tarfile.TarInfo(name)
		
		fp.seek(0, 2)
		tarinfo.size = fp.tell()
		fp.seek(0)
		
		tarinfo.mtime = time.time()
		
		tar.addfile(tarinfo, fp)
	
	def write_tgz(self, book, path, name = None):
		tar = tarfile.open(path, "w:gz")
	
		fp = StringIO()
		formatter = SpecFormatter(fp)
		formatter.book(book, name)
		self._addfile(tar, 'book.devhelp', fp)
	
		for name in book.archive:
			fp = book.archive[name]
			self._addfile(tar, 'book/' + name, fp)
	
	def write(self, book, path, name=None):
		if not path.endswith('.tgz'):
			raise NotImplementedError
		self.write_tgz(book, path, name=None)

	def list(self, **options):
		result = []
		for dir in self.path:
			if os.path.isdir(dir):
				for name in os.listdir(dir):
					path = os.path.join(dir, name, name + '.devhelp')
					if os.path.isfile(path):
						result.append(path)
		return result


"""wxWindows' HTML Help."""


import os.path
import zipfile

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

from htmlhelp.book import Book
from htmlhelp.archive.zip import ZipArchive
from htmlhelp.format import Format
from htmlhelp.format.mshh import HHPParser, MshhFilterArchive, Formatter


#######################################################################
# Format

class HtbFormat(Format):
	
	def __init__(self):
		Format.__init__(self, 'htb')
		
	def read_htb(self, path):
		"""wxWindows HTML Help """
	
		name = os.path.splitext(os.path.basename(path))[0]
	
		archive = ZipArchive(path)
			
		book =  Book(name, archive)
		
		names = [name for name in archive.keys() if name[-4:].lower() == '.hhp']
		if not len(names):
			raise ValueError, 'no HHP file found.'
		if len(names) > 1:
			# FIXME: Actually the HTB format allows more than one project inside a zip
			raise ValueError, 'HTB with multiple books are not supported'
		hhp = names[0]
	
		parser = HHPParser(book)
		parser.parse(archive[hhp])
			
		book.archive = MshhFilterArchive(archive)
	
		return book
	
	def read(self, path, **options):
		if path.endswith('.htb') or path.endswith('.zip'):
			return self.read_htb(path)
		else:
			raise ValueError, 'unknown extension \'%s\'' % path
	
	def write_htb(self, book, path):
		zip_ = zipfile.ZipFile(path, 'w')
	
		name = book.name
			
		formatter = Formatter(book, name)
		
		fp = StringIO()
		formatter.write_hhp(fp)
		zip_.writestr(name + '.hhp', fp.getvalue())
		
		fp = StringIO()
		formatter.write_hhc(fp)
		zip_.writestr(name + '.hhc', fp.getvalue())
		
		fp = StringIO()
		formatter.write_hhk(fp)
		zip_.writestr(name + '.hhk', fp.getvalue())
		
		for name in book.archive:
			fp = book.archive[name]
			zip_.writestr(name, fp.read())
		
	def write(self, book, path, **options):
		if not path.endswith('.htb'):
			raise NotImplementedError
		self.write_htb(book, path)

"""Microsoft Compiled HTML Help (CHM)."""


import sys
import os
import os.path
import struct
import tempfile
import shutil
import subprocess

from htmlhelp.book import Book
from htmlhelp.archive.chm_ import ChmArchive
from htmlhelp.archive.filter import FilterArchive
from htmlhelp.format import Format
from htmlhelp.format.mshh import HHCParser, HHKParser, Formatter



#######################################################################
# Parsing


class SystemParser:

	def __init__(self, book):
		self.book = book
	
		self.parse(self.book.archive['#SYSTEM'])
		
	def read(self, fp, fmt):
		fmt = '<' + fmt
		size = struct.calcsize(fmt)
		data = fp.read(size)
		if not data:
			raise IOError
		return struct.unpack(fmt, data)
	
	def parse(self, fp):
		version, = self.read(fp, 'L')

		try:
			while 1:
				code, length = self.read(fp, 'HH')
				data, = self.read(fp, '%ds' % length)
				data = data.rstrip('\0')
				self.handle_entry(code, data)
		except IOError:
			pass

	def handle_entry(self, code, data):
		if code == 0:
			parser = HHCParser(self.book)
			parser.parse(self.book.archive[data])
		elif code == 1:
			parser = HHKParser(self.book)
			parser.parse(self.book.archive[data])
		elif code == 2:
			self.book.contents.link = data
		elif code == 3:
			self.book.contents.name = data
		

#######################################################################
# Archive filters


class ChmFilterArchive(FilterArchive):

	def filter(self, path):
		if path[:1] in "$#" or path.lower().endswith('.hhc') or path.lower().endswith('.hhk'):
			return None
		return path


#######################################################################
# Format


class ChmFormat(Format):

	def __init__(self):
		Format.__init__(self, 'chm')

	def read_chm(self, path):
		archive = ChmArchive(path)

		name = os.path.splitext(os.path.basename(path))[0]

		book = Book(name, archive)

		SystemParser(book)
		
		for name in archive:
			if name.lower().endswith('.hhc') and not len(book.contents):
				parser = HHCParser(book)
				parser.parse(archive[name])
			elif name.lower().endswith('.hhk') and not len(book.index):
				parser = HHKParser(book)
				parser.parse(archive[name])

		book.archive = ChmFilterArchive(archive)

		return book

	def read(self, path, **options):
		if path.endswith('.chm'):
			return self.read_chm(path)
		else:
			raise ValueError, 'not a CHM file'

	def write_chm(self, book, path):
		dir_ = tempfile.mkdtemp()
		
		name = book.name
			
		formatter = Formatter(book, name)
		
		hhp_name = os.path.join(dir_, name + '.hhp')
		fp = file(hhp_name, 'wt')
		formatter.write_hhp(fp)
		fp.close()
		
		fp = file(os.path.join(dir_, name + '.hhc'), 'wt')
		formatter.write_hhc(fp)
		fp.close()
		
		fp = file(os.path.join(dir_, name + '.hhk'), 'wt')
		formatter.write_hhk(fp)
		fp.close()
		
		for pname in book.archive:
			# FIXME: make parent dirs
			fp = file(os.path.join(dir_, pname), 'wb')
			fp.write(book.archive[pname].read())
			fp.close()

		hhc = 'C:\\Program Files\\HTML Help Workshop\\hhc.exe'
		if sys.platform.startswith('win'):
			subprocess.call([hhc, hhp_name])
		else:
			hhp_name = subprocess.Popen(["winepath", "-w", hhp_name], stdout=subprocess.PIPE).communicate()[0]
			hhp_name = hhp_name.rstrip('\r\n')
			subprocess.call(['wine', hhc, hhp_name])

		shutil.move(os.path.join(dir_, name + '.chm'), path)
		
		shutil.rmtree(dir_)

	def write(self, book, path, **options):
		if not path.endswith('.chm'):
			raise NotImplementedError
		self.write_chm(book, path)


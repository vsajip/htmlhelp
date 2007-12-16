"""Zip archives support."""


import zipfile

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

from htmlhelp.archive import Archive


class ZipArchive(Archive):
	"""Zip archives.

    This class is an adaptor for the python zipfile module."""

	def __init__(self, path):
		Archive.__init__(self)
		
		try:
			self.zip = zipfile.ZipFile(path, "r")
		except zipfile.BadZipfile, msg:
			raise ValueError, msg
		except IOError, msg:
			raise ValueError, msg

	def __getitem__(self, path):
		return StringIO(self.zip.read(path))

	def keys(self):
		return self.zip.namelist()



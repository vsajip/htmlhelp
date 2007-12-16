"""Tarballs archives support."""


import tarfile

from htmlhelp.archive import Archive


class TarArchive(Archive):
	"""Tarball archive.

    This class is an adaptor for the python tarfile module."""

	def __init__(self, path):
		Archive.__init__(self)

		self.tar = tarfile.open(path, 'r')

	def __iter__(self):
		for member in self.tar.getmembers():
			if member.isfile():
				yield member.name
		raise StopIteration

	def __getitem__(self, path):
		return self.tar.extractfile(path)


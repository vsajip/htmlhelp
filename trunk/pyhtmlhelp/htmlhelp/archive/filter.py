"""Archive filtering support."""


from htmlhelp.archive import Archive


class FilterArchive(Archive):
	"""Archive decorator which hides unwanted files from the client and/or
	translates the paths."""

	def __init__(self, archive):
		Archive.__init__(self)

		self.archive = archive
		
	def __iter__(self):
		for path in self.archive:
			path = self.filter(path)
			if path is not None:
				yield path
		raise StopIteration

	def __getitem__(self, path):
		path = self.translate(path)
		if path is None:
			raise KeyError, 'member file access denied'
		return self.archive[path]

	def filter(self, path):
		"""It should return the path under which this file should be seen by the
		client, or None if should be hidden.

		It should be overriden by inherited classes."""

		return path

	def translate(self, path):
		"""It should return the real path of the file, or None if access should
		be denied.

		It should be overriden by inherited classes."""

		return path

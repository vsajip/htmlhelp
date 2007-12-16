"""Archives abstraction and support."""


class Archive:
	"""Presents a dictionary-like view (so far read-only) of a file archive,
	where the keys are file names and the values are file-like objects."""

	# TODO: Add write support
	
	def __init__(self):
		pass

	def __contains__(self, path):
		"""Whether a member with the given path is in the archive or not."""

		for _path in self:
			if _path == path:
				return True
		return False

	def __iter__(self):
		"""Iterate over the member file names.
		
		Should be overrided by derived classes."""
		
		return iter(self.keys())

	def __len__(self):
		count = 0
		for path in self:
			count += 1
		return count

	def __getitem__(self, path):
		"""Get a file-like object for a member in the archive.
		
		Must be overrided by derived classes."""

		raise NotImplementedError

	def __str__(self):
		return str(self.keys())
		
	def has_key(self, path):
		"""Whether a member with the given path is in the archive."""

		return path in self

	def iterkeys(self):
		"""Iterate over the member file names."""
		
		return iter(self)

	def iteritems(self):
		"""Iterate over the member file names."""
		
		for name in self:
			yield name, self[name]
		
		raise StopIteration

	def keys(self):
		"""List archive contents."""
		
		return list(iter(self))
	
	def get(self, path, default=None):
		"""Get a file-like object for a member in the archive."""
		
		try:
			return self[path]
		except KeyError:
			return default


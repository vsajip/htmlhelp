"""Format abstraction."""

__docformat__ = 'epytext'


class Format:
	"""Abstract format.
	
	@ivar name: Format reference name."""
	
	def __init__(self, name):
		self.name = name
	
	def read(self, path, **options):
		"""Read a book from the specified path. A ValueError exception should 
		be raised if the book cannot be read.
		
		@type path: string
		@param path: The path to read the book from.
		@rtype: L{htmlhelp.book.Book}
		@return: A book instance.
		"""
		
		raise ValueError
	
	def write(self, book, path, **options):
		"""Write a book to the specified path. A NotImplementedError exception
		should be raised if this method is not supported.
		
		@type book: L{htmlhelp.book.Book}
		@param book: The book to write.
		@type path: string
		@param path: The path to write the book to.
		"""
		
		raise NotImplementedError

	def list(self, **options):
		"""List available books in this format."""
		
		return []

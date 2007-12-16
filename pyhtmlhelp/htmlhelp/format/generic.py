"""Generic interface to all formats."""


from htmlhelp.format import Format


class GenericFormat(Format):

	def __init__(self):
		Format.__init__(self, 'generic')
		
		self.formats = {}
		
		# FIXME: Do this automatically.
		try:
			from htmlhelp.format.chm import ChmFormat
			self.register(ChmFormat())
		except ImportError:
			pass			
		from htmlhelp.format.devhelp import DevhelpFormat
		self.register(DevhelpFormat())
		from htmlhelp.format.htb import HtbFormat
		self.register(HtbFormat())
		from htmlhelp.format.mshh import MshhFormat
		self.register(MshhFormat())
		from htmlhelp.format.xml_ import XmlFormat
		self.register(XmlFormat())
	
	def register(self, format):
		"""Register this format."""
		
		self.formats[format.name] = format
	
	def read(self, path, **options):
		for format in self.formats.itervalues():
			try:
				return format.read(path, **options)
			except ValueError:
				pass
	
		raise ValueError, 'could not read book from %s' % path
	
	def write(self, book, path, **options):
		for format in self.formats.itervalues():
			try:
				return format.write(book, path, **options)
			except NotImplementedError:
				pass
	
		raise NotImplementedError, 'could not write to book to %s' % path
	

"""HTML based used interface."""


import os.path, posixpath, mimetypes

from HTMLHelp import Book


if __name__ == '__main__':
	import sys
	root = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
	root = os.path.dirname(os.path.abspath(__file__))


def guess_type(path):
	base, ext = posixpath.splitext(path)
	if ext in mimetypes.types_map:
		return mimetypes.types_map[ext]
	else:
		return 'application/octet-stream'


def escape(s):
	"""Helper to add special character quoting."""
	
	s = s.replace("&", "&amp;") # Must be first
	s = s.replace("<", "&lt;")
	s = s.replace(">", "&gt;")
	s = s.replace("'", "&apos;")
	s = s.replace('"', "&quot;")

	return s


def encode(u, encoding = 'iso8859-1'):
	"""Encode a Unicode string in HTML."""
	

	u = u.replace(u"&", u"&amp;") # Must be first

	try:
		s = u.encode(encoding)
	except ValueError:
		s = ''
		for c in u:
			try:
				s += c.encode(encoding)
			except ValueError:
				#if rentitydefs.has_key(c):
				#	s += '&%s;' % rentitydefs[c]
				#else:
					s += '&#%o;' % ord(c)
	s = s.replace("<", "&lt;")
	s = s.replace(">", "&gt;")

	return s


class HTMLError(Exception):
	"""Exception raised for all generation errors."""

	def __init__(self, code, message=None):
		self.code = code
		self.message = message

	def __str__(self):
		return "code %d, message %s" % (self.code, self.message)
		return result


class Request:
	"""The attributes and methods expected from a request object."""

	def __init__(self, path, query):
		self.path = path
		self.query = query

	def set_response(self, code, message=None):
		raise NotImplementedError

	def set_header(self, keyword, value):
		raise NotImplementedError

	def write(self, data):
		raise NotImplementedError
		
	def finish(self):
		raise NotImplementedError


class Resource:

	def __init__(self):
		self.children = {}

	def _child(self, path):
		raise NotImplementedError
	
	def child(self, path):
		if path == '' or path == '.':
			return self
		elif path == '..':
			return None
		elif path in self.children:
			return self.children[path]
		else:
			return self._child(path)
	
	def render(self, request):
		raise NotImplementedError
	

class BlankResource(Resource):

	def _child(self, none):
		return None

	def render(self, request):
		request.set_response(200)
		request.set_header('Content-Type', 'text/html')
		request.write(
			'<html>\n'
			'<head>\n'
			'</head>\n'
			'<body>\n'
			'</body>\n'
			'</html>\n')
		request.finish()


class FileResource(Resource):
	
	def __init__(self, path):
		Resource.__init__(self)

		self.path = path

	def _child(self, path):
		return None

	def render(self, request):
		request.set_response(200)
		request.set_header('Content-Type', guess_type(self.path))
		fp = file(self.path)
		while 1:
			buf = fp.read(8192)
			if not buf:
				break
			request.write(buf)
		request.finish()


class DirectoryResource(Resource):

	def __init__(self, path):
		Resource.__init__(self)

		self.path = path

	def _child(self, path):
		path = posixpath.join(self.path, path)
		if os.path.isdir(path):
			return DirectoryResource(path)
		else:
			return FileResource(path)
	
	def render(self, request):
		request.set_response(400)
		request.set_header('Content-Type', 'text/html')
		# FIXME: fill in here
		request.write(
			'<html>\n'
			'<head>\n'
			'</head>\n'
			'<body>\n'
			'</body>\n'
			'</html>\n')
		request.finish()


class BookPageResource(Resource):

	def __init__(self, book, path):
		Resource.__init__(self)

		self.book = book
		self.path = path

	def _child(self, book, path):
		path = os.path.join(self.path, path)
		return BookPageResource(self.book, path)

	def render(self, request):
		request.set_response(200)
		request.set_header('Content-Type', guess_type(self.path))
		fp = self.book.archive.open(self.path)
		while 1:
			buf = fp.read(8192)
			if not buf:
				break
			request.write(buf)
		request.finish()


index = ['index.html', 'index.htm']


class BookResource(Resource):

	def __init__(self, book):
		Resource.__init__(self)

		self.book = book
	
	def _child(self, path):
		return BookPageResource(self.book, path)
		
	def render(self, request):
		query = request.query
		
		if 'action' not in query:
			self.render_top(request)
		else:
			action = query['action'][-1]
			if action == 'contents':
				self.render_contents(request)
			else:
				request.set_response(400)
				request.set_header('Content-Type', 'text/html')
				request.write(
					'<html>\n'
					'<head>\n'
					'\t<title>Error</title>\n'
					'</head>\n'
					'<body>\n'
					'\t<h1>Error</h1>\n'
					'\t<p>Unknown action: %s</p>\n'
					'</body>\n'
					'</html>\n' % action)
				request.finish()
		
	def render_top(self, request):
		request.set_response(200)
		request.set_header('Content-Type', 'text/html')
		request.write(
			'<html>\n'
			'<head>\n'
			'\t<title>%s</title>\n'
			'</head>\n'
			'\t\t<frameset cols="250,*">\n'
			'\t\t<frame src="?action=contents" name="navigation">\n'
			'\t<frame src="%s" name="main">\n'
			'\t</frameset>\n'
			'</html>\n' % (encode(self.book.title), escape(self.book.default_link)))
		request.finish()

	def render_contents(self, request):
		request.set_response(200)
		request.set_header('Content-Type', 'text/html')
		request.write(
			'<html>\n'
			'<head>\n'
			'\t<title>%s</title>\n'
			'\t<link href="../styles/tree.css" type="text/css" rel="stylesheet" />\n'
			'\t<script type="text/javascript" src="../scripts/tree.js" />\n'
			'</head>\n'
			'<body>\n' % encode(self.book.title))

		request.write('<ul>\n')
		self.walk_contents(request, self.book.contents)
		request.write('</ul>\n')
		
		request.write(
			'</body>\n'
			'</html>\n')
		request.finish()
	
	def walk_contents(self, f, entry, level = 1):
		for subentry in entry:
			if len(subentry):
				f.write('\t'*level + '<li class="closed">')
				f.write('<a href="%s" target="main">%s</a>' % (escape(subentry.link), encode(subentry.name)))
				f.write('\n')
				f.write('\t'*level + '<ul class="closed">\n')
				self.walk_contents(f, subentry, level + 1)
				f.write('\t'*level + '</ul>\n')
				f.write('\t'*level + '</li>\n')
			else:
				f.write('\t'*level + '<li class="none">')
				f.write('<a href="%s" target="main">%s</a>' % (escape(subentry.link), encode(subentry.name)))
				f.write('</li>\n')
				
	
	def render_index(self, request):
		request.set_response(200)
		request.set_header('Content-Type', 'text/html')
		request.write(
			'<html>\n'
			'<head>\n'
			'\t<title>%s</title>\n'
			'\t<link href="../styles/tree.css" type="text/css" rel="stylesheet" />\n'
			'\t<script type="text/javascript" src="../scripts/tree.js" />\n'
			'</head>\n'
			'<body>\n' % encode(self.book.title))

		self.walk_index(request, self.book.index)
		
		request.write(
			'</body>\n'
			'</html>\n')
		request.finish()
	
	def walk_index(self, f, entry, level = 1):
		f.write('\t'*level)
		if level == 1:
			f.write('<ul>\n')
		else:
			f.write('<ul class="closed">\n')
		for child in entry:
			f.write('\t'*(level + 1))
			if len(child):
				f.write('<li class="closed">')
			else:
				f.write('<li class="none">')
			f.write('<a href="%s" target="main">%s</a>' % (escape(child.link), encode(child.name)))
			if child.children:
				f.write('\n')
				self.walk_index(f, child, level + 1)
				f.write('\t'*(level + 1))
			f.write('</li>\n')
		f.write('\t'*level + '</ul>\n')
	


class CatalogResource(Resource):

	def __init__(self, catalog):
		Resource.__init__(self)

		self.catalog = catalog

		for path in ('icons', 'scripts', 'styles'):
			self.children[path] = DirectoryResource(os.path.join(root, path))

	def _child(self, path):
		if path in self.catalog:
			entry = self.catalog[path]
			return BookResource(entry.book)
		else:
			return None

	def render(self, request):
		request.set_response(200)
		request.set_header('Content-Type', 'text/html')
		request.write(
			'<html>\n'
			'<head>\n'
			'\t<title>HTML Help Books</title>\n'
			'</head>\n'
			'<body>\n'
			'\t<h1>HTML Help Books</h1>\n'
			'\t<ul>\n')
		for entry in self.catalog:
			request.write('\t\t<li><a href="%s/">%s</a></li>' % (entry.name, entry.name))
		request.write(
			'\t</ul>\n'
			'</body>\n'
			'</html>\n')
		request.finish()


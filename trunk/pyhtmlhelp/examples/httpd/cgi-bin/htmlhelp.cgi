#!/usr/bin/python


if __name__ == "__main__":
	import cgitb
	cgitb.enable()


import cgi, os, shutil, sys

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

sys.path.insert(0, '.')
sys.path.insert(0, '..')
from HTMLHelp import Formats
import HTML


class Request(HTML.Request):

	def __init__(self):
		path = os.getenv('PATH_INFO', '')[1:]
		query = cgi.parse()

		HTML.Request.__init__(self, path, query)

		self.code = 200
		self.message = None
		self.headers = {}
		self.fp = StringIO()
	
	def set_response(self, code, message = None):
		self.code = code
		self.message = message
	
	def set_header(self, name, value):
		self.headers[name] = value
	
	def write(self, data):
		self.fp.write(data)

	def finish(self):
		for name, value in self.headers.iteritems():
			sys.stdout.write('%s: %s\n' % (name, value))
		sys.stdout.write('\n')
		buf = self.fp.getvalue()
		sys.stdout.write(buf)


def main():
	catalog = Formats.catalog
	resource = HTML.CatalogResource(catalog)
	
	request = Request()
	path = request.path
	for path in request.path.split('/'):
		resource = resource.child(path)
		if resource is None:
			sys.stdout.write('Content-Type: text/html\n')
			sys.stdout.write('\n')
			sys.stdout.write(
				'<html>\n'
				'<head>\n'
				'\t<title>Error</title>\n'
				'</head>\n'
				'<body>\n'
				'\t<h1>Error</h1>\n'
				'\t<p>Not found: %s</p>\n'
				'</body>\n'
				'</html>\n' % request.path)
			return
	
	resource.render(request)


if __name__ == "__main__":
	main()


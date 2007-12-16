#!/usr/bin/python


import cgi, os.path, posixpath, sys, urllib, urlparse, BaseHTTPServer

from HTMLHelp import Formats
import HTML


if 0:

	try:
		from cStringIO import StringIO
	except ImportError:
		from StringIO import StringIO


	class Request(HTML.Request):

		def __init__(self, handler):
			scheme, netloc, path, query, fragment = urlparse.urlsplit(handler.path)
			path = posixpath.normpath(urllib.unquote(path))
			query = cgi.parse_qs(query)

			HTML.Request.__init__(self, path, query)

			self.handler = handler

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
			self.handler.send_response(self.code, self.message)
			for name, value in self.headers.iteritems():
				self.handler.send_header(name, value)
			self.handler.end_headers()
			if self.handler.command != 'HEAD':
				buf = self.fp.getvalue()
				self.handler.wfile.write(buf)
else:

	class Request(HTML.Request):
		# This one relies on the exact ordering of the call to the
		# methods to work without caching the request response

		def __init__(self, handler):
			scheme, netloc, path, query, fragment = urlparse.urlsplit(handler.path)
			path = posixpath.normpath(urllib.unquote(path))
			query = cgi.parse_qs(query)

			HTML.Request.__init__(self, path, query)

			self.handler = handler

			self.finished_headers = 0
			
		
		def set_response(self, code, message = None):
			self.handler.send_response(code, message)
		
		def set_header(self, name, value):
			self.handler.send_header(name, value)
		
		def write(self, data):
			if not self.finished_headers:
				self.handler.end_headers()
				self.finished_headers = 1
				
			if self.handler.command != 'HEAD':
				self.handler.wfile.write(data)

		def finish(self):
			if not self.finished_headers:
				self.handler.end_headers()


class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	catalog = Formats.catalog
	resource = HTML.CatalogResource(catalog)
	
	def do(self):
		request = Request(self)
		path = request.path
		resource = self.resource
		for path in request.path.split('/'):
			resource = resource.child(path)
			if resource is None:
				self.send_error(404)
				return

		resource.render(request)
	
	do_HEAD = do_GET = do
	

def main():
	BaseHTTPServer.test(MyRequestHandler)


if __name__ == "__main__":
	main()

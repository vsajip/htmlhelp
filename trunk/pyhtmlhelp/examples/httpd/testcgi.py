#!/usr/bin/python


import sys
import CGIHTTPServer


def main():
	class MyRequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):

		def _is_cgi(self):
			path = self.path

			x = '/cgi-bin/htmlhelp.cgi'
			i = len(x)
			if path[:i] == x and (not path[i:] or path[i] == '/'):
				self.cgi_info = '', path[1:i]
				return 1
			return 0
	
	CGIHTTPServer.test(MyRequestHandler)
	

if __name__ == "__main__":
	main()


#!/usr/bin/python
# -*- coding: iso8859-1 -*-
"""Modified CGI HTTP server to handle PHP scripts."""


__author__ = "José Fonseca"


import os
import urllib
import CGIHTTPServer
import posixpath


class PHPHTTPRequestHandler(CGIHTTPServer.CGIHTTPRequestHandler):

	indices = [
		'index.html', 
		'index.cgi', 
		'index.pl', 
		'index.php', 
		'index.xhtml',
	]
	
	aliases = [
		('/', './'),
		('/cgi-bin', '/usr/lib/cgi-bin'),
	]

	actions = {
		'application/x-httpd-php': '/cgi-bin/php4',
	}

	CGIHTTPServer.CGIHTTPRequestHandler.extensions_map.update({
		'.php': 'application/x-httpd-php',
	})
	
	def do_HEAD(self):
		self.redirect_path()
		CGIHTTPServer.CGIHTTPRequestHandler.do_HEAD(self)
		
	def do_GET(self):
		self.redirect_path()
		CGIHTTPServer.CGIHTTPRequestHandler.do_GET(self)
		
	def do_POST(self):
		self.redirect_path()
		CGIHTTPServer.CGIHTTPRequestHandler.do_POST(self)
		
	def redirect_path(self):
		path = self.path
		i = path.rfind('?')
		if i >= 0:
			path, query = path[:i], path[i:]
		else:
			query = ''

		head, tail = path, ''
		temp = self.translate_path(head)
		while not os.path.exists(temp):
			i = head.rfind('/')
			if i < 0:
				break
			head, tail = head[:i], head[i:] + tail
			temp = self.translate_path(head)

		if os.path.isdir(temp):
			for index in self.indices:
				if os.path.exists(os.path.join(temp, index)):
					head = posixpath.join(head, index)
					break

		ctype = self.guess_type(head)
		if ctype in self.actions:
			os.environ['REDIRECT_STATUS'] = '200'			
			head = self.actions[ctype] + head

		self.path = head + tail + query

	def translate_path(self, path):
		path = posixpath.normpath(urllib.unquote(path))
		n = len(self.aliases)
		for i in range(n):
			url, dir = self.aliases[n-i-1]
			length = len(url)
			if path[:length] == url:
				return dir + path[length:]
		return ''


if __name__ == '__main__':
	CGIHTTPServer.test(PHPHTTPRequestHandler)

#!/usr/bin/python

from distutils.core import setup

setup(
	name = "pyhtmlhelp",
	version = "0.5",
	description = 'HTML Help Books Python API',
	author = 'Jose Fonseca',
	author_email = 'jose.r.fonseca@gmail.com',
	url = 'http://htmlhelp.googlecode.com/',
	packages = [
		'htmlhelp',
		'htmlhelp.archive',
		'htmlhelp.format',
		'htmlhelp.util',
	],
	scripts = [
		'hhconvert.py',
	],
)

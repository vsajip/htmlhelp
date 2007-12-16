#!/usr/bin/env python


import unittest
import formattest

from htmlhelp.format.devhelp import *


class DevhelpTestCase(formattest.SampleFormatTestCase):
	
	format = DevhelpFormat()
	
	paths = [
		'data/sample_book.devhelp',
		'data/sample_book.tgz']
	
	exts = ['tgz']

	def failUnlessEqualMetadata(self, a, b):
		pass
	

if __name__ == '__main__':
	unittest.main()

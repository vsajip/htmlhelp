#!/usr/bin/env python


import unittest
import formattest

from htmlhelp.format.chm import *


class ChmTestCase(formattest.SampleFormatTestCase):
	
	format = ChmFormat()
	
	paths = [
		'data/sample_book.chm']

	exts = []

	def failUnlessEqualMetadata(self, a, b):
		pass
	

if __name__ == '__main__':
	unittest.main()

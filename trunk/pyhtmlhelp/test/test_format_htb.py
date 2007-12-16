#!/usr/bin/env python


import unittest
import formattest

from htmlhelp.format.htb import *


class HtbTestCase(formattest.SampleFormatTestCase):
	
	format = HtbFormat()
	
	paths = [
		'data/sample_book.htb']
	
	exts = ['htb']

	def failUnlessEqualMetadata(self, a, b):
		pass
	

if __name__ == '__main__':
	unittest.main()

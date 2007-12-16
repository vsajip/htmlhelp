#!/usr/bin/env python


import unittest
import formattest

from htmlhelp.format.mshh import *


class MshhTestCase(formattest.SampleFormatTestCase):
	
	format = MshhFormat()
	
	paths = [
		'data/sample_book.hhp']

	exts = []

	def failUnlessEqualMetadata(self, a, b):
		pass
	

if __name__ == '__main__':
	unittest.main()

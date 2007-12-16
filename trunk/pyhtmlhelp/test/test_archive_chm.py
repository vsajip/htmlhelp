#!/usr/bin/env python


import unittest
import archivetest

from htmlhelp.archive.chm_ import ChmArchive
from htmlhelp.archive.filter import FilterArchive


class ChmArchiveTestCase(archivetest.SampleArchiveTestCase):
	
	def setUp(self):
		self.archive = ChmArchive('data/sample_archive.chm')
	

if __name__ == '__main__':
	unittest.main()

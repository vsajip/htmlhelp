#!/usr/bin/env python


import unittest
import archivetest

from htmlhelp.archive.zip import ZipArchive


class ZipArchiveTestCase(archivetest.SampleArchiveTestCase):
	
	def setUp(self):
		self.archive = ZipArchive('data/sample_archive.zip')
	

if __name__ == '__main__':
	unittest.main()

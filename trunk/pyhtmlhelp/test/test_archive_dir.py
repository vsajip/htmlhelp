#!/usr/bin/env python


import unittest
import archivetest

from htmlhelp.archive.dir import DirArchive


class DirArchiveTestCase(archivetest.SampleArchiveTestCase):
	
	def setUp(self):
		self.archive = DirArchive('data/sample_archive')
	

if __name__ == '__main__':
	unittest.main()

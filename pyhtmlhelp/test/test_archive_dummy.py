#!/usr/bin/env python


import unittest
import archivetest

from htmlhelp.archive.dummy import DummyArchive


class DummyArchiveTestCase(archivetest.ArchiveTestCase):
	
	def setUp(self):
		self.archive = DummyArchive()
	

if __name__ == '__main__':
	unittest.main()

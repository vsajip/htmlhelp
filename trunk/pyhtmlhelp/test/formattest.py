"""Base test case for formats."""


import sys
import os
import unittest


class FormatTestCase(unittest.TestCase):

	def failUnlessEqualArchive(self, a, b):
		self.failUnless(len(a) >= len(b))
		for name in b:
			afile = a[name]
			bfile = b[name]
			self.failUnlessEqual(afile.read(), bfile.read())
		
	def failUnlessEqualContents(self, a, b):
		self.failUnlessEqual(a.name, b.name)
		self.failUnlessEqual(a.link, b.link)
		self.failUnlessEqual(len(a), len(b))
		for achild, bchild in zip(a, b):
			self.failUnlessEqualContents(achild, bchild)
			
	def failUnlessEqualIndex(self, a, b):
		self.failUnlessEqual(len(a), len(b))
		for aterm, bterm in zip(a, b):
			self.failUnlessEqual(aterm.name, bterm.name)
			self.failUnlessEqual(aterm.links, bterm.links)
	
	def failUnlessEqualMetadata(self, a, b):
		# NOTE: this method should be overriden if metadata is not supported by format under test
		self.failUnlessEqual(a, b)
	
	def failUnlessEqualBook(self, a, b):
		self.failUnlessEqualContents(a.contents, b.contents)
		self.failUnlessEqualIndex(a.index, b.index)
		self.failUnlessEqualArchive(a.archive, b.archive)
		self.failUnlessEqualMetadata(a.metadata, b.metadata)
		
		
class SampleFormatTestCase(FormatTestCase):

	def setUp(self):
		# Get the expected sample book from the automatically generated 
		# Python code.
		from data import sample_book
		self.sample_book = sample_book.book
	
	def testRead(self):
		# Read the books in the several format variants and tests whether they 
		# match agains the expected one.
		for book in [self.format.read(path) for path in self.paths]:
			self.failUnlessEqualBook(book, self.sample_book)
	
	def testWrite(self):
		# Write the sample book to a temporary file, read it back, and test if
		# it matches with the source.
		for ext in self.exts:
			if sys.platform == "win32":
				tmpdir = os.environ["TEMP"]
			else:
				tmpdir = "/tmp"
			path = os.path.join(tmpdir, 'test.' + ext)
			self.format.write(self.sample_book, path)
			book = self.format.read(path)
			self.failUnlessEqualBook(book, self.sample_book)



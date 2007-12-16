"""Base test case for archives."""


import unittest


class ArchiveTestCase(unittest.TestCase):
	# This test suite will check of the methods of an Archive instance
	# are return coherent information.
	
	missing_path = 'AVeryUnlikelyFileName'
	
	def failUnlessFileObj(self, fp, path):
		# Fail if fp is not a read file-like object.
	
		# Given Python dynamic type system it is not enough to verify if fp is an
		# instance of 'file'. Instead we verify if all the usual file reading 
		# methods exist.
		for method in [
				'close',
				'read',
				'readline',
				'seek',
				'tell']:
			self.failUnless(hasattr(fp, method), "'%s' method is missing from '%s' file" % (method, path))
			self.failUnless(callable(getattr(fp, method)), "'%s' method is not callable '%s' file" % (method, path))
	
	def setUp(self):
		# Must be overriden by subclasses and set self.archive to an instance 
		# of the Archive class.
		raise NotImplementedError
		
	def testContains(self):
		# Iterates every file in the archive and tests if it is reported as 
		# present. Also tests a file which is guaranteed not be in the archive and 
		# tests if it is reported as missing.
		for path in self.archive:
			self.failUnless(path in self.archive, "'%s' is listed in the archive but reported as missing" % path)
		self.failIf(self.missing_path in self.archive, "'%s' should be reported as missing" % self.missing_path)

	def testGetItem(self):
		# Iterates every file in the archive and tests if it can be read. Also 
		# tests a file which is guaranteed not be in the archive and tests if it an 
		# exception is throw.
		for path in self.archive:
			try:
				fp = self.archive[path]
			except KeyError:
				self.fail("'%s' is listed in the archive but not accessible" % path)
			self.failUnlessFileObj(fp, path)
				
		try:
			fp = self.archive[self.missing_path]
			self.fail("'%s' should not be accessible" % self.missing_path)
		except KeyError:
			pass
	
	def testLen(self):
		# Tests whether the reported archive length matches the one found by 
		# iterating through the archive.
		l = 0
		for path in self.archive:
			l += 1
		self.failUnlessEqual(len(self.archive), l)


class SampleArchiveTestCase(ArchiveTestCase):
	# This test suite expects a sample archive with determined content and will
	# if that holds true, regardless of the concrete archive type.

	paths = [
		'empty',
		'file',
		'dir/file',
		'dir/subdir/file']
	
	def testList(self):
		# Test if every expected file is present.
		for path in self.paths:
			self.failUnless(path in self.archive, "'%s' is missing" % path)

	# NOTE: this can not be guaranteed at the moment
	#def testLen2(self):
	#	# Test if only the expected files are present.
	#	self.failUnlessEqual(len(self.archive), len(self.paths))
			
	def testEmpty(self):
		# Tests if an empty file is correctly read as empty.
		fp = self.archive['empty']
		self.failUnlessEqual(fp.read(), '')
	
	def testFile(self):
		# Tests if the regular files are correctly read.
		for path in [
				'file',
				'dir/file',
				'dir/subdir/file']:
			fp = self.archive[path]
			self.failUnlessEqual(fp.read(), 'Sample...\n')

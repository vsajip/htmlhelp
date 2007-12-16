#!/usr/bin/env python


import os
import unittest


def main():
	suite = unittest.TestSuite()
	for name in os.listdir('.'):
		if name.startswith('test_') and name.endswith('.py'):
			suite.addTest(unittest.defaultTestLoader.loadTestsFromName(name[:-3]))
	unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
	main()

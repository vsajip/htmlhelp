#!/usr/bin/env python
"""Export a HTML Help book into another format."""


import optparse

from htmlhelp.format.generic import GenericFormat


def main():
	parser = optparse.OptionParser(usage="\n\t%prog [options] src dst", version="%prog 1.0")
	(options, args) = parser.parse_args()
	if len(args) != 2:
		parser.error("incorrect number of arguments")

	format = GenericFormat()

	input = args[0]
	output = args[1]
	
	book = format.read(input)

	format.write(book, output)


if __name__ == '__main__':
	main()

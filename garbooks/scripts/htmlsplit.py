#!/usr/bin/env python


import re
import sys


def normalize_space(s):
	"""Normalize whitespace."""

	return ' '.join(s.split())


html_entity_re = re.compile(r'&(?:([a-zA-Z][-.a-zA-Z0-9]*)|#(?:([0-9]+)|[xX]([0-9a-fA-F]+)));?')

html_parts_re = re.compile(r'(.*?<body(?:\s.*?)?>)(.*?)(</body\s*>.*?)', re.IGNORECASE | re.DOTALL)

html_title_re = re.compile(r'<title(?:\s.*?)?>(.*?)</title\s*>', re.IGNORECASE | re.DOTALL)

html_headings_re = re.compile(r'<h[2-4]><a .*?name="(.*?)".*?>(.*?)</h[2-4]>', re.IGNORECASE | re.DOTALL)

html_anchors_re = re.compile(r'<a .*?name="(.*?)".*?>', re.IGNORECASE | re.DOTALL)

html_tag_re = re.compile(r'<.*?>', re.DOTALL)

def htmlsplit(filename):
	html = file(filename).read()

	mo = html_parts_re.match(html)

	header = mo.group(1)
	body = mo.group(2)
	footer = mo.group(3)

	parts = {}
	titles = {}
	
	title = None
	name = 'index'
	spos = 0
	epos = 0
	while 1:
		mo = html_headings_re.search(body, epos)
		if mo:
			epos = mo.start(0)
		else:
			epos = len(body)
		
		parts[name] = body[spos:epos]
		titles[name] = title
		
		if mo:
			name = mo.group(1)
			title = mo.group(2)
			
			assert name not in parts

			spos = epos
			epos = mo.end(0)
		else:
			break

	anchors = {}

	for name, part in parts.iteritems():
		for anchor in html_anchors_re.findall(part):
			assert anchor not in anchors
			anchors[anchor] = name
	
	for name, part in parts.iteritems():
		for anchor, link in anchors.iteritems():
			part = part.replace('"#' + anchor + '"', '"' + link + '.html#' + anchor + '"')
		parts[name] = part

	for name, part in parts.iteritems():
		title = titles[name]
		fp = file(name + '.html', 'w')
		mo = html_title_re.search(header)
		if title and mo:
			fp.write(header[:mo.start(1)])
			fp.write(normalize_space(html_tag_re.sub(' ', title)))
			fp.write(header[mo.end(1):])
		else:
			fp.write(header)
		fp.write(part)
		fp.write(footer)
		

def main():
	for arg in sys.argv[1:]:
		htmlsplit(arg)


if __name__ == '__main__':
	main()


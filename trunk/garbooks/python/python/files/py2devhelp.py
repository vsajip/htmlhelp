#!/usr/bin/python

'''
    Makes the necessary files to convert from plain html of
    Python 1.5 and 1.5.x Documentation to devhelp book
    Doesn't change the html's docs.

    by hernan.foffani@iname.com
    no copyright and no responsabilities.

    modified by Dale Nagata for Python 1.5.2

    modified by Christian Tismer for Python 2.0

    modified by Jose Fonseca for generating devhelp

'''

import sys
import os
import formatter
import htmllib
import string
import getopt



# moved all the triple_quote up here because my syntax-coloring editor
# sucks a little bit.
usage_mode = '''
Usage: py2devhelp.py [-c] [-f] [-v 1.5[.x]] filename
    -c: does not include the table of contents
    -f: does not include the function table
    -v 1.5[.x]: makes help for the python 1.5[.x] docs
        (default is python 2.3 docs)
'''

# Library Doc list of tuples:
# each 'book' : ( Dir, Title, First page, Content page, Index page)
#
supported_libraries = {
    # j_r_fonseca@yahoo.co.uk Mar 15/07: library for 2.5 version:
    '2.5':
    [
        Book('.', 'Main page', 'index'),
        Book('.', 'Global Module Index', 'modindex'),
        Book('whatsnew', "What's New", 'index', 'contents'),
        Book('tut','Tutorial','tut','node2'),
        Book('lib','Library Reference','lib','contents','genindex'),
        Book('ref','Language Reference','ref','contents','genindex'),
        Book('mac','Macintosh Reference','mac','contents','genindex'),
        Book('ext','Extending and Embedding','ext','contents'),
        Book('api','Python/C API','api','contents','genindex'),
        Book('doc','Documenting Python','doc','contents'),
        Book('inst','Installing Python Modules', 'inst', 'index'),
        Book('dist','Distributing Python Modules', 'dist', 'index', 'genindex'),
    ],

    # j_r_fonseca@yahoo.co.uk Sep 29/05: library for 2.4 version:
    '2.4':
    [
        ('tut','Tutorial','tut.html','node2.html',None),
        ('whatsnew','What\'s New','whatsnew24.html','contents.html',None),
        ('.','Global Module Index','modindex.html',None,None),
        ('lib','Library Reference','lib.html','contents.html','genindex.html'),
        ('ref','Language Reference','ref.html','contents.html','genindex.html'),
        ('mac','Macintosh Module Reference','mac.html','contents.html','genindex.html'),
        ('ext','Extending and Embedding','ext.html','contents.html',None),
        ('api','Python/C API','api.html','contents.html','genindex.html'),
        ('doc','Documenting Python','doc.html','contents.html',None) ,
        ('inst','Installing Python Modules','inst.html','index.html',None),
        ('dist','Distributing Python Modules','dist.html','index.html','genindex.html'),
    ],

    # j_r_fonseca@yahoo.co.uk Aug 21/03: library for 2.3 version:
    '2.3':
    [
        ('tut','Tutorial','tut.html','node2.html',None),
        ('whatsnew','What\'s New','whatsnew23.html','contents.html',None),
        ('.','Global Module Index','modindex.html',None,None),
        ('lib','Library Reference','lib.html','contents.html','genindex.html'),
        ('ref','Language Reference','ref.html','contents.html','genindex.html'),
        ('mac','Macintosh Module Reference','mac.html','contents.html','genindex.html'),
        ('ext','Extending and Embedding','ext.html','contents.html',None),
        ('api','Python/C API','api.html','contents.html','genindex.html'),
        ('doc','Documenting Python','doc.html','contents.html',None) ,
        ('inst','Installing Python Modules','inst.html','index.html',None),
        ('dist','Distributing Python Modules','dist.html','index.html',None),
    ],

    # hernan@orgmf.com.ar Nov 28/01: library for 2.2 version:
    '2.2':
    [
        ('tut','Tutorial','tut.html','node2.html',None),
        ('.','Global Module Index','modindex.html',None,None),
        ('lib','Library Reference','lib.html','contents.html','genindex.html'),
        ('ref','Language Reference','ref.html','contents.html','genindex.html'),
        ('mac','Macintosh Module Reference','mac.html','contents.html','genindex.html'),
        ('ext','Extending and Embedding','ext.html','contents.html',None),
        ('api','Python/C API','api.html','contents.html','genindex.html'),
        ('doc','Documenting Python','doc.html','contents.html',None) ,
        ('inst','Installing Python Modules','inst.html','index.html',None),
        ('dist','Distributing Python Modules','dist.html','index.html',None),
    ],

    # hernan@orgmf.com.ar Apr 17/01: library for 2.1 version:
    '2.1':
    [
        ('tut','Tutorial','tut.html','node2.html',None),
        ('.','Global Module Index','modindex.html',None,None),
        ('lib','Library Reference','lib.html','contents.html','genindex.html'),
        ('ref','Language Reference','ref.html','contents.html','genindex.html'),
        ('mac','Macintosh Module Reference','mac.html','contents.html','genindex.html'),
        ('ext','Extending and Embedding','ext.html','contents.html',None),
        ('api','Python/C API','api.html','contents.html','genindex.html'),
        ('doc','Documenting Python','doc.html','contents.html',None) ,
        ('inst','Installing Python Modules','inst.html','index.html',None),
        ('dist','Distributing Python Modules','dist.html','index.html',None),
    ],

    # tismer@tismer.com Nov 26/00: library for 2.0 version:
    '2.0':
    [
        ('tut','Tutorial','tut.html','node2.html',None),
        ('.','Global Module Index','modindex.html',None,None),
        ('lib','Library Reference','lib.html','contents.html','genindex.html'),
        ('ref','Language Reference','ref.html','contents.html','genindex.html'),
        ('mac','Macintosh Module Reference','mac.html','contents.html','genindex.html'),
        ('ext','Extending and Embedding','ext.html','contents.html',None),
        ('api','Python/C API','api.html','contents.html','genindex.html'),
        ('doc','Documenting Python','doc.html','contents.html',None) ,
        ('inst','Installing Python Modules','inst.html','contents.html',None),
        ('dist','Distributing Python Modules','dist.html','contents.html',None),
    ],

    # <dnagata@creo.com> Apr 17/99: library for 1.5.2 version:
    # <hernan.foffani@iname.com> May 01/99: library for 1.5.2 (04/30/99):
    '1.5.2':
    [
        ('tut','Tutorial','tut.html','node2.html',None),
        ('lib','Library Reference','lib.html','contents.html','genindex.html'),
        ('ref','Language Reference','ref.html','contents.html','genindex.html'),
        ('mac','Macintosh Reference','mac.html','contents.html','genindex.html'),
        ('ext','Extending and Embedding','ext.html','contents.html',None),
        ('api','Python/C API','api.html','contents.html','genindex.html'),
        ('doc','Documenting Python','doc.html','contents.html',None)
    ],

    # library for 1.5.1 version:
    '1.5.1':
    [
        ('tut','Tutorial','tut.html','contents.html',None),
        ('lib','Library Reference','lib.html','contents.html','genindex.html'),
        ('ref','Language Reference','ref-1.html','ref-2.html','ref-11.html'),
        ('ext','Extending and Embedding','ext.html','contents.html',None),
        ('api','Python/C API','api.html','contents.html','genindex.html')
    ],

    # library for 1.5 version:
    '1.5':
    [
        ('tut','Tutorial','tut.html','node1.html',None),
        ('lib','Library Reference','lib.html','node1.html','node268.html'),
        ('ref','Language Reference','ref-1.html','ref-2.html','ref-11.html'),
        ('ext','Extending and Embedding','ext.html','node1.html',None),
        ('api','Python/C API','api.html','node1.html','node48.html')
    ]
}

class AlmostNullWriter(formatter.NullWriter):
    savedliteral = ''

    def send_flowing_data(self, data):
        # need the text tag for later
        datastriped = string.strip(data)
        if self.savedliteral == '':
            self.savedliteral = datastriped
        else:
            self.savedliteral = string.strip(self.savedliteral +
                                            ' ' + datastriped)

entitydefs = {'amp': 'amp', 'lt':'lt', 'gt':'gt', 'quot':'quot'}

class HelpHtmlParser(htmllib.HTMLParser):
    indent = 1  # number of tabs for pretty printing of files
    ft = None   # output file
    path = None # relative path
    proc = 0    # if true I process, if false I skip
                #   (some headers, footers, etc.)

    def begin_group(self):
        if not self.proc:
            # first level, start processing
            self.proc = 1
        self.indent = self.indent + 1

    def finish_group(self):
        self.indent = self.indent - 1
        if self.proc and self.indent == 1:
            # if processing and back to root, then stop
            self.proc = 0

    def anchor_bgn(self, href, name, type):
        if self.proc == 1:
            self.formatter.writer.savedliteral = ''
            self.ft.write('\t' * self.indent + '<sub link="' + self.path + '/' + href + '"')
	self.proc = self.proc + 1

    def anchor_end(self):
	self.proc = self.proc - 1
        if self.proc == 1:
            name = self.formatter.writer.savedliteral
            self.ft.write(' name="' + name + '">\n')

    def start_dl(self, atr_val):
        self.begin_group()

    def end_dl(self):
        self.finish_group()

    def handle_entityref(self, ref):
	if entitydefs.has_key(ref):
		self.handle_data('&' + entitydefs[ref] + ';')
	else:
		htmllib.HTMLParser.handle_data(self, ref)


class IdxHlpHtmlParser(HelpHtmlParser):
    prevname = ''

    def anchor_bgn(self, href, name, type):
        if self.proc == 1:
            self.formatter.writer.savedliteral = ''
            self.ft.write('\t<function link="' + self.path + '/' + href + '"')
	self.proc = self.proc + 1

    def anchor_end(self):
	self.proc = self.proc - 1
        if self.proc == 1:
            import string
            name = self.formatter.writer.savedliteral
            if name != '[Link]':
                self.prevname = name
            else:
                name = self.prevname

            self.ft.write(' name="' + name + '"/>\n')


class TocHlpHtmlParser(HelpHtmlParser):
    flag = 0

    def start_dl(self, atr_val):
        self.begin_group()
        self.flag = 0

    def end_dl(self):
        if self.flag:
            self.ft.write('\t' * self.indent + '</sub>\n')
        self.finish_group()
        self.flag = 1

    def do_dt(self, atr_val):
        if self.flag:
            self.ft.write('\t' * self.indent + '</sub>\n')
        self.flag = 1

    def start_ul(self, atr_val):
        self.begin_group()
        self.flag = 0

    def end_ul(self):
        if self.flag:
            self.ft.write('\t' * self.indent + '</sub>\n')
        self.finish_group()
        self.flag = 1

    def do_li(self, atr_val):
        if self.flag:
            self.ft.write('\t' * self.indent + '</sub>\n')
        self.flag = 1


def index(path, archivo, output):
    f = formatter.AbstractFormatter(AlmostNullWriter())
    parser = IdxHlpHtmlParser(f)
    parser.path = path
    parser.ft = output
    fil = path + '/' + archivo
    parser.feed(open(fil).read())
    parser.close()


def content(path, archivo, output):
    f = formatter.AbstractFormatter(AlmostNullWriter())
    parser = TocHlpHtmlParser(f)
    parser.path = path
    parser.ft = output
    fil = path + '/' + archivo
    parser.feed(open(fil).read())
    parser.close()


def do_index(library, output):
    output.write('<functions>\n')
    for book in library:
        print '\t', book[2]
        if book[4]:
            index(book[0], book[4], output)
    output.write('</functions>\n')


def do_content(library, output):
    output.write('<chapters>\n')
    for book in library:
        print '\t', book[2]
        output.write('\t<sub name="%s" link="%s">\n' % (book[1], book[0]+"/"+book[2]))
        if book[3]:
            content(book[0], book[3], output)
        output.write('\t</sub>\n')
    output.write('</chapters>\n')



def openfile(file):
    try:
        p = open(file, "w")
    except IOError, msg:
        print file, ":", msg
        sys.exit(1)
    return p

def usage():
        print usage_mode
        sys.exit(0)

def do_it(args = None):
    if not args:
        args = sys.argv[1:]

    if not args:
        usage()

    try:
        optlist, args = getopt.getopt(args, 'cfv:')
    except getopt.error, msg:
        print msg
        usage()

    if not args or len(args) > 1:
        usage()
    arch = args[0]

    # default to 2.3
    version = '2.3'
    for opt in optlist:
        if opt[0] == '-v':
            version = opt[1]
            break
    library = supported_libraries[ version ]
    #print version, library

    f = openfile(arch + '.devhelp')
    f.write('<?xml version="1.0" encoding="iso-8859-1"?>\n\n')
    f.write('<book title="Python Documentation" name="Python" version="%s" link="index.html">\n\n' % ((version)))

    if not (('-c','') in optlist):
        print "Building Table of Content..."
        do_content(library, f)

    if not (('-f','') in optlist):
        print "Building Index..."
        do_index(library, f)

    f.write('</book>\n')
    f.close()

if __name__ == '__main__':
    do_it()


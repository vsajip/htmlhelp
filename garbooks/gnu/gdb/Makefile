GARNAME = gdb
GARVERSION = 6.6
MASTER_SITES = \
	http://ftp.gnu.org/pub/gcc/$(GARNAME)/ \
	ftp://sources.redhat.com/pub/$(GARNAME)/releases/
DISTFILES = $(GARNAME)-$(GARVERSION).tar.bz2

CONFIGURE_SCRIPTS = $(WORKSRC)/gdb/configure

BUILD_SCRIPTS = $(WORKSRC)/gdb/doc/Makefile
BUILD_ARGS = clean gdb.info
	
BOOKS = \
	$(WORKSRC)/gdb/doc/gdb.texinfo \

NOINST_BOOKS = \
	$(WORKSRC)/gdb/doc/gdbint.texinfo \
	$(WORKSRC)/gdb/doc/stabs.texinfo

include ../../gar.mk

TEXI2HTML_FLAGS = -I $(WORKSRC)/gdb/mi -I $(WORKSRC)/readline/doc


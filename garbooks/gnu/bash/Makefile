GARNAME = bash
GARVERSION = 3.2
MASTER_SITES = http://ftp.gnu.org/pub/gnu/$(GARNAME)/
DISTFILES = $(GARNAME)-$(GARVERSION).tar.gz

BOOKS = $(WORKSRC)/doc/bashref.texi

include ../../gar.mk

TEXI2HTML_FLAGS += -I $(WORKSRC)/lib/readline/doc

GARNAME = gettext
GARVERSION = 0.16
MASTER_SITES = http://ftp.gnu.org/pub/gnu/$(GARNAME)/
DISTFILES = $(GARNAME)-$(GARVERSION).tar.gz

BOOKS = \
	$(WORKSRC)/gettext-tools/doc/gettext.texi \
	$(WORKSRC)/gettext-tools/libasprintf/autosprintf.texi

include ../../gar.mk

TEXI2HTML_FLAGS += -I $(WORKSRC)/gettext-runtime/doc

GARNAME = gpc
GARVERSION = 2.1
MASTER_SITES = http://www.gnu-pascal.de/stable/
DISTFILES = $(GARNAME)-$(GARVERSION).tar.gz

WORKSRC = $(WORKDIR)/$(GARNAME)-20020510/p

BOOKS = $(WORKSRC)/doc/en/gpc.texi

include ../../gar.mk

%/$(WORKSRC)/doc/en/gpc.texi: BOOK_EXTRAS = $(addsuffix :,$(wildcard $(WORKSRC)/doc/images/*.png))


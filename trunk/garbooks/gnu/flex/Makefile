GARNAME = flex
GARVERSION = 2.5.34
MASTER_SITES = http://heanet.dl.sourceforge.net/sourceforge/$(GARNAME)/
DISTFILES = $(GARNAME)-$(GARVERSION).tar.bz2

BOOKS = $(WORKSRC)/MISC/texinfo/flex.texi

include ../../gar.mk

$(WORKDIR)/flex.texi: $(WORKSRC)/MISC/texinfo/flex.texi
	sed -e "s/@section/@chapter/g" $< > $@

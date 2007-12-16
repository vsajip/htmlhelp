GARNAME = css
GARVERSION = 2.1
MASTER_SITES = http://www.w3.org/TR/CSS21/
DISTFILES = css2.tgz

BOOKS = css

include ../../gar.mk

extract-css2.tgz: $(WORKSRC)

extract: EXTRACTDIR = $(WORKSRC)

convert-devhelp/css:
	rm -rf $(SCRATCHDIR)
	mkdir -p $(SCRATCHDIR)
	cp -a $(FILEDIR)/css.devhelp $(SCRATCHDIR)/book.devhelp
	cp -a $(WORKSRC) $(SCRATCHDIR)/book
	@$(MAKECOOKIE)


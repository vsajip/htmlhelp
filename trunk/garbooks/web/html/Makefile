GARNAME = html
GARVERSION = 4.01
MASTER_SITES = http://www.w3.org/TR/html401/
DISTFILES = html40.tgz 

BOOKS = html

include ../../gar.mk

extract-html40.tgz: $(WORKSRC)

extract: EXTRACTDIR = $(WORKSRC)

convert-devhelp/html:
	rm -rf $(SCRATCHDIR)
	mkdir -p $(SCRATCHDIR)
	cp -a $(FILEDIR)/html.devhelp $(SCRATCHDIR)/book.devhelp
	cp -a $(WORKSRC) $(SCRATCHDIR)/book
	@$(MAKECOOKIE)


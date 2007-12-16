GARNAME = xhtml
GARVERSION = 1.0
MASTER_SITES = http://www.w3.org/TR/xhtml1/
DISTFILES = xhtml1.tgz 

BOOKS = xhtml

include ../../gar.mk

WORKSRC = $(WORKDIR)/xhtml1-20020801

convert-devhelp/xhtml:
	rm -rf $(SCRATCHDIR)
	mkdir -p $(SCRATCHDIR)
	cp -a $(FILEDIR)/xhtml.devhelp $(SCRATCHDIR)/book.devhelp
	cp -a $(WORKSRC) $(SCRATCHDIR)/book
	rm -f $(SCRATCHDIR)/book/*.ps
	rm -f $(SCRATCHDIR)/book/*.pdf
	@$(MAKECOOKIE)


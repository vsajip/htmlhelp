GARNAME = xslt
GARVERSION = 1.0
MASTER_SITES = http://www.w3.org/TR/1999/
DISTFILES = REC-xslt-19991116.html

BOOKS = xslt

include ../../gar.mk

convert-devhelp/xslt:
	rm -rf $(SCRATCHDIR)
	mkdir -p $(SCRATCHDIR)
	cp -a $(FILEDIR)/xslt.devhelp $(SCRATCHDIR)/book.devhelp
	mkdir -p $(SCRATCHDIR)/book
	cd $(SCRATCHDIR)/book && $(CURDIR)/../../scripts/htmlsplit.py $(CURDIR)/$(WORKDIR)/REC-xslt-19991116.html
	@$(MAKECOOKIE)


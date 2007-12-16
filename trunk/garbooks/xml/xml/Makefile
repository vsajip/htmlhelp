GARNAME = xml
GARVERSION = 1.0
MASTER_SITES = fake://
DISTFILES = REC-xml-20040204.html

BOOKS = xml

include ../../gar.mk

fake//REC-xml-20040204.html: 
	wget -c -P  -T 120 -t 3 http://www.w3.org/TR/2004/REC-xml-20040204/ -O $(PARTIALDIR)/REC-xml-20040204.html

convert-devhelp/xml:
	rm -rf $(SCRATCHDIR)
	mkdir -p $(SCRATCHDIR)
	cp -a $(FILEDIR)/xml.devhelp $(SCRATCHDIR)/book.devhelp
	mkdir -p $(SCRATCHDIR)/book
	cd $(SCRATCHDIR)/book && $(CURDIR)/../../scripts/htmlsplit.py $(CURDIR)/$(WORKDIR)/REC-xml-20040204.html
	@$(MAKECOOKIE)


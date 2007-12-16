GARNAME = bzip2
GARVERSION = 1.0.4
MASTER_SITES = http://www.bzip.org/$(GARVERSION)/
DISTFILES = $(GARNAME)-$(GARVERSION).tar.gz

BOOKS = $(WORKSRC)/bzip2.xml

include ../../gar.mk

$(WORKSRC)/bzip2.xml: $(WORKSRC)/manual.xml
	perl $(WORKSRC)/format.pl $< $@

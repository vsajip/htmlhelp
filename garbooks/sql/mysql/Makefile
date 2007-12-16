GARNAME = mysql
GARVERSION = 4.1.22
MASTER_SITES = http://mirrors.sunsite.dk/mysql/Downloads/MySQL-4.1/
DISTFILES = $(GARNAME)-$(GARVERSION).tar.gz

# See also:
#
# http://phlab.net/myman/
# http://phlab.net/html2hhp/

BOOKS = \
	$(WORKSRC)/Docs/manual.texi \
	$(WORKSRC)/Docs/internals.texi

include ../../gar.mk

%/$(WORKSRC)/Docs/manual.texi: BOOK_NAME = mysql_manual
%/$(WORKSRC)/Docs/manual.texi: BOOK_EXTRAS = $(addsuffix :Images,$(wildcard $(WORKSRC)/Docs/Images/*.png))
%/$(WORKSRC)/Docs/manual.texi: BOOK_PATCH = sed -i -e 's:.././Images:Images:g' *.html

%/$(WORKSRC)/Docs/internals.texi: BOOK_NAME = mysql_internals


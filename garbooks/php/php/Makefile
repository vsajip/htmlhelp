GARNAME = php
#GARVERSION = 
MASTER_SITES = cvs://cvsread@cvs.php.net/repository/
DISTFILES = phpdoc
#PATCHFILES = gar-base.diff

# See also:
#   http://www.php.net/manual/howto/
#   http://weblabor.hu/php-doc-chm/

CONFIGURE_SCRIPTS = $(WORKDIR)/phpdoc/configure
CONFIGURE_ARGS = --with-chm=yes --with-xsl=yes

BUILD_SCRIPTS = $(WORKDIR)/phpdoc/Makefile
BUILD_ARGS = chm_xsl

BOOKS = $(WORKDIR)/phpdoc/htmlhelp/php_manual_en.mshh

include ../../gar.mk

checksum-phpdoc:
	$(DONADA)

pre-configure:
	cd $(WORKDIR)/phpdoc && autoconf
	$(MAKECOOKIE)

convert-mshh/phpdoc:
	rm -rf $(SCRATCHDIR)
	ln -sf html $(SCRATCHDIR)

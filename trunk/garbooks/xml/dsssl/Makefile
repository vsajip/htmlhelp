GARNAME = dsssl
MASTER_SITES = ftp://ftp.ornl.gov/pub/sgml/wg8/$(GARNAME)/
DISTFILES = helpsrc.zip
PATCHFILES = gar-base.diff

BOOKS = dsssl

WORKSRC = $(WORKDIR)/helpsrc

include ../../gar.mk

convert-mshh/dsssl:
	@rm -rf $(SCRATCHDIR)
	@cp -a $(WORKSRC) $(SCRATCHDIR)
	@$(MAKECOOKIE)

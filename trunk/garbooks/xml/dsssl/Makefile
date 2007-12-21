GARNAME = dsssl
MASTER_SITES = http://xml.coverpages.org/
DISTFILES = dsssl-walsh-helpsrc.zip
PATCHFILES = gar-base.diff

BOOKS = dsssl

WORKSRC = $(WORKDIR)/helpsrc

include ../../gar.mk

convert-mshh/dsssl:
	@rm -rf $(SCRATCHDIR)
	@cp -a $(WORKSRC) $(SCRATCHDIR)
	@$(MAKECOOKIE)

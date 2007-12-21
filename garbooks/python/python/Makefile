GARNAME = python
GARVERSION = 2.5.1
MASTER_SITES = http://www.python.org/ftp/python/doc/$(GARVERSION)/
DISTFILES = html-$(GARVERSION).tar.bz2

WORKSRC = $(WORKDIR)/Python-Docs-$(GARVERSION)

BOOKS = python


include ../../gar.mk


PYVERSION = $(basename $(GARVERSION))
#PYVERSION = $(GARVERSION)

convert-devhelp/python: $(FILEDIR)/py2devhelp.py
	@rm -rf $(SCRATCHDIR)
	@mkdir -p $(SCRATCHDIR)
	@cp -a $(WORKSRC) $(SCRATCHDIR)/book
	cd $(SCRATCHDIR)/book && python $(CURDIR)/$(FILEDIR)/py2devhelp.py -v $(PYVERSION) ../book
	@$(MAKECOOKIE)

# See http://svn.python.org/projects/python/trunk/Doc/tools/prechm.py
convert-mshh/python: $(FILEDIR)/prechm.py
	@rm -rf $(SCRATCHDIR)
	@cp -a $(WORKSRC) $(SCRATCHDIR)
	cd $(SCRATCHDIR) && python $(CURDIR)/$(FILEDIR)/prechm.py -v $(PYVERSION) $(GARNAME)
	@$(MAKECOOKIE)

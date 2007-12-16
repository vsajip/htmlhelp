GARNAME = perl
GARVERSION = 5.8.8
MASTER_SITES = http://www.cpan.org/src/
DISTFILES = $(GARNAME)-$(GARVERSION).tar.bz2

define BLURB
 See also:
 - http://search.cpan.org/~swmcd/Pod-Tree-1.10/
 - http://search.cpan.org/~autrijus/Pod-HtmlHelp-1.1/
 - http://search.cpan.org/~pvhp/Pod2WinHlp-0.02/README
endef

BUILD_SCRIPTS = perldoc
BOOKS = perl

include ../../gar.mk

build-perldoc:
	rm -rf $(WORKDIR)/html
	rm -f pod2htmd.tmp pod2htmi.tmp
	for FILE in `grep -l '^=[a-z]' $(WORKSRC)/README.* | sed -e 's/.*\///'`; \
	do \
		NAME=`echo $$FILE | sed -e "s/README\.//"`; \
		rm -f $(WORKSRC)/pod/perl$$NAME.pod; \
		ln -s ../$$FILE $(WORKSRC)/pod/perl$$NAME.pod; \
	done
	perl $(WORKSRC)/installhtml \
		--podroot=$(WORKSRC) \
		--podpath=. \
		--htmldir=$(WORKDIR)/html \
		--htmlroot=/ \
		--splithead=pod/perlipc \
		--splititem=pod/perlfunc \
		--libpods=perlfunc:perlguts:perlvar:perlrun:perlop \
		--recurse \
		--verbose
	rm -f pod2htmd.tmp pod2htmi.tmp
	cp $(FILEDIR)/perl.css $(WORKDIR)/html
	$(SHELL) $(FILEDIR)/addcss.sh perl.css $(WORKDIR)/html
	@$(MAKECOOKIE)

convert-devhelp/perl:
	@rm -rf $(SCRATCHDIR)
	mkdir -p $(SCRATCHDIR)
	cp -a $(WORKDIR)/html $(SCRATCHDIR)/book
	$(SHELL) $(FILEDIR)/perl2devhelp.sh $(SCRATCHDIR) $(GARVERSION) 
	rm -f pod2htmd.tmp pod2htmi.tmp
	@$(MAKECOOKIE)

convert-mshh/perl:
	@rm -rf $(SCRATCHDIR)
	cp -a $(WORKDIR)/html $(SCRATCHDIR)
	$(SHELL) $(FILEDIR)/perl2chm.sh $(SCRATCHDIR)
	@$(MAKECOOKIE)

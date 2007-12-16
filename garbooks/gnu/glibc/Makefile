GARNAME = glibc
GARVERSION = 2.5
MASTER_SITES = http://ftp.gnu.org/pub/gnu/$(GARNAME)/
DISTFILES = $(GARNAME)-$(GARVERSION).tar.bz2
PATCHFILES = gar-base.diff

BUILD_SCRIPTS = $(WORKSRC)/manual/Makefile
BUILD_ARGS = info

BOOKS = $(WORKSRC)/manual/libc.texinfo

include ../../gar.mk

post-extract:
	rm -f $(WORKSRC)/Makeconfig
	@$(MAKECOOKIE)

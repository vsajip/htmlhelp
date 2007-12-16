#-*- mode: Fundamental; tab-width: 4; -*-
# ex:ts=4

# This file contains configuration variables that are global to
# the GAR system.  Users wishing to make a change on a
# per-package basis should edit the category/package/Makefile, or
# specify environment variables on the make command-line.

# Variables that define the default *actions* (rather than just
# default data) of the system will remain in bbc.gar.mk
# (bbc.port.mk)

# If the color codes are interfering with your terminal, consider
# commenting this next line out.

COLOR_GAR ?= yes

# changing this to "yes" will cause the GAR build to use the
# "stow" utility to merge packages into the system tree using
# symlinks.  

USE_STOW ?= no
STOW_PREFIX ?= $(prefix)/stow/

# Setting this variable will cause the results of your builds to
# be cleaned out after being installed.  Uncomment only if you
# desire this behavior!

# export BUILD_CLEAN = true

ALL_DESTIMGS = main build rootbin lnximg singularity

# These are the standard directory name variables from all GNU
# makefiles.  They're also used by autoconf, and can be adapted
# for a variety of build systems.
# 
# TODO: set $(SYSCONFDIR) and $(LOCALSTATEDIR) to never use
# /usr/etc or /usr/var

# Directory config for the "main" image
main_prefix ?= /
main_exec_prefix = $(prefix)
main_bindir = $(exec_prefix)/bin
main_sbindir = $(exec_prefix)/sbin
main_libexecdir = $(exec_prefix)/libexec
main_datadir = $(prefix)/share
main_sysconfdir = $(prefix)/etc
main_sharedstatedir = $(prefix)/share
main_localstatedir = $(prefix)/var
main_libdir = $(exec_prefix)/lib
main_infodir = $(prefix)/info
main_lispdir = $(prefix)/share/emacs/site-lisp
main_includedir = $(prefix)/include
main_mandir = $(prefix)/man
main_docdir = $(prefix)/share/doc
main_sourcedir = $(prefix)/src
main_licensedir = $(prefix)/licenses

# Directory config for the "build" image
build_prefix ?= /tmp/build
build_exec_prefix = $(build_prefix)
build_bindir = $(build_exec_prefix)/bin
build_sbindir = $(build_exec_prefix)/sbin
build_libexecdir = $(build_exec_prefix)/libexec
build_datadir = $(build_prefix)/share
build_sysconfdir = $(build_prefix)/etc
build_sharedstatedir = $(build_prefix)/share
build_localstatedir = $(build_prefix)/var
build_libdir = $(build_exec_prefix)/lib
build_infodir = $(build_prefix)/info
build_lispdir = $(build_prefix)/share/emacs/site-lisp
build_includedir = $(build_prefix)/include
build_mandir = $(build_prefix)/man
build_docdir = $(build_prefix)/share/doc
build_sourcedir = $(build_prefix)/src
build_licensedir = $(build_prefix)/licenses

# the DESTDIR is used at INSTALL TIME ONLY to determine what the
# filesystem root should be.  Each different DESTIMG has its own
# DESTDIR.
main_DESTDIR ?= /tmp/gar
build_DESTDIR ?= /
build_chroot_DESTDIR ?= /tmp/chroot

# allow us to link to libraries we installed
#main_CPPFLAGS += -nostdinc
#main_CFLAGS += -nostdinc -nostdlib
#main_LDFLAGS += -nostdlib
main_CPPFLAGS += $(foreach DESTIMG,main,-I$(DESTDIR)$(includedir))
main_CFLAGS += $(foreach DESTIMG,main,-Os -I$(DESTDIR)$(includedir) -L$(DESTDIR)$(libdir))
#main_CXXFLAGS += $(foreach DESTIMG,main,-Os -I$(DESTDIR)$(includedir) -L$(DESTDIR)$(libdir))
main_LDFLAGS += $(foreach DESTIMG,main,-L$(DESTDIR)$(libdir))
main_CPPFLAGS += $(foreach DESTIMG,main,-I$(GCC_INCLUDEDIR) -I$(CROSS_GCC_INCLUDEDIR))
main_CFLAGS += $(foreach DESTIMG,main,-I$(GCC_INCLUDEDIR) -I$(CROSS_GCC_INCLUDEDIR) -L$(GCC_LIBDIR) -L$(CROSS_GCC_LIBDIR))
#main_CXXFLAGS += $(foreach DESTIMG,main,-I$(GCC_INCLUDEDIR) -I$(CROSS_GCC_INCLUDEDIR) -L$(GCC_LIBDIR) -L$(CROSS_GCC_LIBDIR))
main_LDFLAGS += $(foreach DESTIMG,main,-L$(GCC_LIBDIR) -L$(CROSS_GCC_LIBDIR))

# allow us to link to libraries we installed
build_CPPFLAGS += $(foreach DESTIMG,build,-I$(DESTDIR)$(includedir))
build_CFLAGS += $(foreach DESTIMG,build,-Os -I$(DESTDIR)$(includedir) -L$(DESTDIR)$(libdir))
#build_CXXFLAGS += $(foreach DESTIMG,build,-Os -I$(DESTDIR)$(includedir) -L$(DESTDIR)$(libdir))
build_LDFLAGS += $(foreach DESTIMG,build,-L$(DESTDIR)$(libdir))

# Default main_CC to gcc, $(DESTIMG)_CC to main_CC and set CC based on $(DESTIMG)
main_CC ?= gcc
main_CXX ?= g++
main_LD ?= ld
main_RANLIB ?= ranlib
main_CPP ?= cpp
main_AS ?= as
main_AR ?= ar
build_CC ?= gcc
build_CXX ?= g++
build_LD ?= ld
build_RANLIB ?= ranlib
build_CPP ?= cpp
build_AS ?= as
build_AR ?= ar

# GARCH and GARHOST for main.  Override these for cross-compilation
#main_GARCH ?= $(shell arch)
#main_GARHOST ?= $(shell gcc -dumpmachine)
main_GARCH ?= none
main_GARHOST ?= none

# GARCH and GARHOST for build.  Do not change these.
#build_GARCH := $(shell arch)
#build_GARHOST := $(GARBUILD)
build_GARCH := none
build_GARHOST := none

# Assume that the build system has support for the C and C++ languages and test
# for perl.  Would check for python, too, but python needs to builddep itself.
#build_NODEPEND += lang/c lang/c++
#build_NODEPEND += $(if $(shell which perl),lang/perl,)

# Assume the same of main, also check for python
#main_NODEPEND += lang/c lang/c++
#main_NODEPEND += $(if $(shell which perl),lang/perl,)
#main_NODEPEND += $(if $(shell which python),lang/python,)

# Most stuff is written in C, so SOURCE_LANGUAGES will default to that
#SOURCE_LANGUAGES ?= c

# Profiles other than LNX-BBC should override this in the environment
LNX_FLAVOR ?= bbc

# This is for foo-config chaos
PKG_CONFIG_PATH=$(DESTDIR)$(libdir)/pkgconfig/

# Put these variables in the environment during the
# configure build and install stages
STAGE_EXPORTS = DESTDIR prefix exec_prefix bindir sbindir libexecdir datadir
STAGE_EXPORTS += sysconfdir sharedstatedir localstatedir libdir infodir lispdir
STAGE_EXPORTS += includedir mandir docdir sourcedir
STAGE_EXPORTS += CPPFLAGS CFLAGS LDFLAGS
STAGE_EXPORTS += CC CXX CPP LD RANLIB AS AR

CONFIGURE_ENV += $(foreach TTT,$(STAGE_EXPORTS),$(TTT)="$($(TTT))")
BUILD_ENV += $(foreach TTT,$(STAGE_EXPORTS),$(TTT)="$($(TTT))")
INSTALL_ENV += $(foreach TTT,$(STAGE_EXPORTS),$(TTT)="$($(TTT))")
MANIFEST_ENV += $(foreach TTT,$(STAGE_EXPORTS),$(TTT)="$($(TTT))")

# Global environment
export GARBUILD
export PATH LD_LIBRARY_PATH #LD_PRELOAD
export PKG_CONFIG_PATH

GARCHIVEROOT ?= /var/www/garchive
GARCHIVEDIR = $(GARCHIVEROOT)/$(DISTNAME)
GARPKGROOT ?= /var/www/garpkg
GARPKGDIR = $(GARPKGROOT)/$(GARNAME)

# prepend the local file listing
FILE_SITES = file://$(FILEDIR)/ file://$(GARCHIVEDIR)/

# Extra configuration for the lnx-bbc build
GAR_EXTRA_CONF += htmlhelp.conf.mk

# Extra libs to include with gar.mk
GAR_EXTRA_LIBS += htmlhelp.lib.mk

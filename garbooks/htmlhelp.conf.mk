SHELL=/bin/bash

GARCHIVEROOT = $(GARDIR)/../garchive

COOKIEDIR = $(COOKIEROOTDIR)
WORKDIR = $(WORKROOTDIR)

BOOKARCHIVEROOT ?= $(GARDIR)/../books
BOOKARCHIVEDIR ?= $(BOOKARCHIVEROOT)

#HTMLHELP_EXTRA_LIBS ?= chm.lib.mk devhelp.lib.mk htb.lib.mk
HTMLHELP_EXTRA_LIBS ?= chm.lib.mk

COLOR_GAR = no

main_GARCH = none
main_GARHOST = none
GARBUILD = none

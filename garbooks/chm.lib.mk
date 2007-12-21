# Compiled Html Help books generation


htmlhelp: chm


# chm	- Generate Compiled Html Help books.

CHM_TARGETS = $(addprefix compile-chm/,$(BOOKS))

chm: build pre-chm $(CHM_TARGETS) post-chm
	$(DONADA)

# returns true if the Compiled Html Help books have completed successfully, false otherwise
chm-p:
	@$(foreach COOKIEFILE,$(CHM_TARGETS), test -e $(COOKIEDIR)/$(COOKIEFILE) ;)


##################### CHM RULES ###################

include $(GARDIR)/mshh.lib.mk

HHC = "C:/Program Files/HTML Help Workshop/hhc.exe"
HHC_FLAGS =

ifeq ($(WINDIR),)
HHC := wine $(HHC)
endif

compile-chm/%: post-convert-mshh/%
	@echo -e " $(WORKCOLOR)==> Compiling $(BOLD)$(WORKDIR)/$(BOOK_FILENAME).chm$(NORMALCOLOR)"
	-@$(HHC) $(HHC_FLAGS) $(SCRATCHDIR)/*.hhp
#	-@cd $(SCRATCHDIR) && $(HHC) $(HHC_FLAGS) *.hhp
	@mv $(SCRATCHDIR)/*.chm $(WORKDIR)/$(BOOK_FILENAME).chm
	@rm -rf $(SCRATCHDIR)
	@$(MAKECOOKIE)


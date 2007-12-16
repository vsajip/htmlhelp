# wxWindows HTB books generation
#
# See also:
# 
#   http://www.wxwindows.org/help.htm
#   http://www.wxwindows.org/manuals/2.4.0/wx499.htm#helpformat


htmlhelp: htb


# htb	- Generate Html Help books.

HTB_TARGETS = $(addprefix compile-htb/,$(BOOKS))

htb: build pre-htb $(HTB_TARGETS) post-htb
	$(DONADA)

# returns true if the Compiled Html Help books have completed successfully, false otherwise
htb-p:
	@$(foreach COOKIEFILE,$(HTB_TARGETS), test -e $(COOKIEDIR)/$(COOKIEFILE) ;)


##################### HTB RULES ###################

include $(GARDIR)/mshh.lib.mk

compile-htb/%: post-convert-mshh/%
	@echo -e " $(WORKCOLOR)==> Compiling $(BOLD)$(WORKDIR)/$(BOOK_FILENAME).zip$(NORMALCOLOR)"
	cd $(SCRATCHDIR) && zip -qr $(CURDIR)/$(WORKDIR)/$(BOOK_FILENAME).zip .
	@rm -rf $(SCRATCHDIR)
	@$(MAKECOOKIE)

error-htb/%:
	@echo -e "$(ERRORCOLOR)*** Don't know how to build HTB book from $* ***$(NORMALCOLOR)"

compile-htb/%: error-htb/%
	@true

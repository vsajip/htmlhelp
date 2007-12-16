# DevHelp books generation


htmlhelp: devhelp


# devhelp	- Generate DevHelp books.

DEVHELP_TARGETS = $(addprefix compile-devhelp/,$(BOOKS))

devhelp: build pre-devhelp $(DEVHELP_TARGETS) post-devhelp
	$(DONADA)

# returns true if DevHelp books have completed successfully, false otherwise
devhelp-p:
	@$(foreach COOKIEFILE,$(DEVHELP_TARGETS), test -e $(COOKIEDIR)/$(COOKIEFILE) ;)


#################### DEVHELP RULES ####################

# DocBook SGML

JADE = jade
JADE_FLAGS = \
	-V %devhelp-name%="$*" \
	-V %devhelp-version%="$(VERSION)"

DEVHELP_DSL = $(GARDIR)/stylesheets/docbook/devhelp.dsl

ifdef DSSSL
DSSSL_ = $(WORKDIR)/devhelp.dsl

$(DSSSL_): $(DEVHELP_DSL)
	sed -e "s@docbook\.dsl@$(DSSSL)@" $< > $@
else
DSSSL_ = $(DEVHELP_DSL)
endif

sgml-devhelp/%: %
	@echo -e " $(WORKCOLOR)==> Converting $(BOLD)$*$(NORMALCOLOR)"
	@cd $(*D) && $(JADE) -t sgml -i html $(JADE_FLAGS) -d $(DSSSL_) $(DCL) $(*F)
	@mv $(basename $*)/$(basename $(*F)).devhelp $(SCRATCHDIR)/book.devhelp
	@mv $(basename $*) $(SCRATCHDIR)/book


# DocBook XML (using XSL)

XSLTPROC = xsltproc 
XSLTPROC_FLAGS = 
XSLTPROC_FLAGS_DEVHELP = \
	--stringparam "devhelp.name" "$(*F)" \
	--stringparam "devhelp.version" "$(GARVERSION)"

DEVHELP_XSL = $(GARDIR)/stylesheets/docbook/devhelp.xsl

ifdef XSL
XSL_ = $(WORKDIR)/devhelp.xsl

$(XSL_): $(DEVHELP_XSL)
	sed -e "s@docbook\.xsl@$(XSL)@" $< > $@
else
XSL_ = $(DEVHELP_XSL)
endif

xml-devhelp/%: %
	$(XSLTPROC) $(XSLTPROC_FLAGS) $(XSLTPROC_FLAGS_DEVHELP) -o $(SCRATCHDIR)/ $(XSL_) $*


# Texinfo (using texi2html)

TEXI2HTML = texi2html
TEXI2HTML_FLAGS = 
TEXI2HTML_FLAGS_DEVHELP = --init-file devhelp.init

texi-devhelp/%: %
	@echo -e " $(WORKCOLOR)==> Converting $(BOLD)$*$(NORMALCOLOR)"
	$(TEXI2HTML) $(TEXI2HTML_FLAGS) $(TEXI2HTML_FLAGS_DEVHELP) --prefix $(BOOK_NAME) --out $(SCRATCHDIR)/book --css-include $(GARDIR)/stylesheets/import_texinfo.css $*
	@cp -a $(GARDIR)/stylesheets/texinfo.css $(SCRATCHDIR)/book
	@mv $(SCRATCHDIR)/book/$(BOOK_NAME).devhelp $(SCRATCHDIR)/book.devhelp


# Common targets

pre-convert-devhelp/%:
	rm -rf $(SCRATCHDIR)
	mkdir -p $(SCRATCHDIR)

convert-devhelp/%: pre-convert-devhelp/% 

convert-devhelp/%.sgml: pre-convert-devhelp/% sgml-devhelp/%.sgml
	@true

convert-devhelp/%.texi: pre-convert-devhelp/% texi-devhelp/%.texi
	@true

convert-devhelp/%.texinfo: pre-convert-devhelp/% texi-devhelp/%.texinfo
	@true

convert-devhelp/%.txi: pre-convert-devhelp/% texi-devhelp/%.txi
	@true

convert-devhelp/%.xml: pre-convert-devhelp/% xml-devhelp/%.xml
	@true

post-convert-devhelp/%: convert-devhelp/% 
	@$(foreach BOOK_EXTRA,$(BOOK_EXTRAS), \
		mkdir -p $(SCRATCHDIR)/book/$(BOOK_EXTRA_DST); \
		cp -a $(BOOK_EXTRA_SRC) $(SCRATCHDIR)/book/$(BOOK_EXTRA_DST);)
	@cd $(SCRATCHDIR)/book/ ; $(BOOK_PATCH)

compile-devhelp/%: post-convert-devhelp/%
	@echo -e " $(WORKCOLOR)==> Validating $(BOLD)$(SCRATCHDIR)/book.devhelp$(NORMALCOLOR)"
	@xmllint --noout --dtdvalid ../../scripts/devhelp-1.dtd $(SCRATCHDIR)/book.devhelp
	@echo -e " $(WORKCOLOR)==> Compiling $(BOLD)$(WORKDIR)/$(BOOK_FILENAME).tgz$(NORMALCOLOR)"
	@tar -czf $(WORKDIR)/$(BOOK_FILENAME).tgz -C $(SCRATCHDIR) book.devhelp book
	@rm -rf $(SCRATCHDIR)
	@$(MAKECOOKIE)

error-devhelp/%:
	@echo -e "$(ERRORCOLOR)*** Don't know how build a DevHelp book from $* ***$(NORMALCOLOR)"
	@$(MAKECOOKIE)

compile-devhelp/%: error-devhelp/%
	@true


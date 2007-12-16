GARNAME = gtk
MASTER_SITES = http://developer.gnome.org/doc/API/
DISTFILES = \
	glib-2.0-docs.tar.gz \
	gobject-2.0-docs.tar.gz \
	pango-1.0-docs.tar.gz \
	atk-1.0-docs.tar.gz \
	gdk-pixbuf-2.0-docs.tar.gz \
	gdk-2.0-docs.tar.gz \
	gtk-2.0-docs.tar.gz

BOOKS = glib gobject pango atk gdk-pixbuf gdk gtk

include ../../gar.mk

$(addprefix convert-devhelp/,$(BOOKS)):
	@rm -rf $(SCRATCHDIR)
	@mkdir -p $(SCRATCHDIR)
	cp -a $(WORKDIR)/$(notdir $@) $(SCRATCHDIR)/book
	mv $(SCRATCHDIR)/book/$(notdir $@).devhelp $(SCRATCHDIR)/book.devhelp
	sed -i -e '/^<!DOCTYPE /d' $(SCRATCHDIR)/book.devhelp
	rm -f $(SCRATCHDIR)/book/index.sgml
	@$(MAKECOOKIE)


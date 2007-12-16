GARNAME = gnome
MASTER_SITES = \
	http://developer.gnome.org/doc/API/ \
	http://www.gnome.org/~mathieu/libart/ \
	http://librsvg.sourceforge.net/docs/
DISTFILES = \
	at-spi-1.0-docs.tar.gz \
	gail-1.0-docs.tar.gz \
	libglade-2.0-docs.tar.gz \
	libgnome-2.0-docs.tar.gz \
	libgnomeui-2.0-docs.tar.gz \
	gnome-vfs-2.0-docs.tar.gz \
	gconf-2.0-docs.tar.gz \
	libgnomecanvas-2.0-docs.tar.gz \
	libart-docs.tar.gz \
	ORBit-2.0-docs.tar.gz \
	bonobo-activation-docs.tar.gz \
	libbonobo-docs.tar.gz \
	libbonoboui-docs.tar.gz

# XXX: These don't work:
#	vte-doc.tar.gz \
	panel-applet-doc.tar.gz \
	libgsf-docs.tar.gz

BOOKS =  \
	at-spi-cspi \
	bonobo-activation \
	gail-libgail-util \
	gconf \
	gnome-vfs-2.0 \
	libbonobo \
	libbonoboui \
	libglade \
	libgnomecanvas \
	libgnome \
	libgnomeui \
	ORBit2

include ../../gar.mk

$(addprefix convert-devhelp/,$(BOOKS)):
	@rm -rf $(SCRATCHDIR)
	@mkdir -p $(SCRATCHDIR)
	cp -a $(WORKDIR)/$(notdir $@) $(SCRATCHDIR)/book
	mv $(SCRATCHDIR)/book/$(notdir $@).devhelp $(SCRATCHDIR)/book.devhelp
	sed -i -e '/^<!DOCTYPE /d' $(SCRATCHDIR)/book.devhelp
	rm -f $(SCRATCHDIR)/book/index.sgml
	@$(MAKECOOKIE)


# About #

[DevHelp](http://www.imendio.com/projects/devhelp/) is a GNOME based online help system aimed toward developers.

# Format #

It uses a XML spec file to store the table of contents, the index, and book metadata. For more information about the XML format see:

  * [DevHelp DTD](http://cvs.gnome.org/lxr/source/devhelp/dtd/devhelp-1.dtd)
  * [README for DevHelp](http://cvs.gnome.org/lxr/source/devhelp/README)

The books usually are distributed in a GZip'd tarball (`.tgz`) but they must decompressed before read by ''DevHelp''.

# Authoring #

  * The [GTK Documentation Tools](ftp://ftp.gtk.org/pub/gtk/v1.1/docs/rdp) a XSL stylesheet that automatically generates the DevHelp spec for the GTK and GNOME documentation.

# Viewers #

DevHelp is before all a help viewer. See its [homepage](http://www.imendio.com/projects/devhelp/) for more information about it.

# Miscellaneous #

  * [devhelp2chm.sh](http://htmlhelp.googlecode.com/svn/trunk/misc/devhelp2chm.sh) — is a script to convert DevHelp bookname into a CHM file, written by Ralgh Young.

# Links #
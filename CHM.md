# Authoring #

The [Microsoft HTML Help 1.3 SDK](http://msdn.microsoft.com/library/en-us/htmlhelp/html/vsconHH1Start.asp) is the official way to create CHM's. The HTML Help Compiler (HHC) takes a HTML Help Project (HHP) file with metadata, a HTML Help Contents (HHC) with the table of contents, and a HTML Help Index (HHK) with the index keywords, and the HTML pages, producing a CHM.

[HTML Help Maker](http://bonedaddy.net/pabs3/hhm/) is an open-source project which plans to allow the creation of CHM's

Many open-source tools automatically generate the HHP, HHC, and HHK together with the HTML output. Especially worth noting are:

  * [DocBook XSL Stylesheets](http://docbook.sourceforge.net/projects/xsl/index.html)
  * [Doxygen](http://www.doxygen.org/)
  * [texi2html](http://ximbiot.com/texi2html/)

# Format #

Microsoft never released the format specification, but there are a few reverse engineered descriptions of the format:

  * [Unofficial CHM Specification](http://savannah.nongnu.org/projects/chmspec)
  * Matthew Russotto's [Microsoft's HTML Help format](http://www.speakeasy.org/~russotto/chm/chmformat.html) description

There are some tools which allow to read the contents of CHM files:

  * [CHMLIB](http://66.93.236.84/~jedwin/projects/chmlib/)
  * [libmspack](http://www.cabextract.org.uk/libmspack/) — a library for Microsoft compression formats

# Viewers #

  * Microsoft HTML Help Viewer
  * [xCHM](http://xchm.sourceforge.net/) — a CHM viewer for UNIX (Linux, BSD, Solaris), written by Razvan Cojocaru
  * [JouleData Solutions' CHM Viewer](http://www.jouledata.com/MacProducts.html) — a comercial 100% native Cocoa .chm file viewer for the Mac OS X platform
  * [GnoCHM](http://gnochm.sourceforge.net/) — a CHM file viewer. It is designed to integrate nicely with Gnome.
  * [chmviewer](http://www.herdsoft.com/linux/themen/chmviewer.html)
  * [ChmSee](http://chmsee.gro.clinux.org/)
  * [Chmox](http://chmox.sourceforge.net/) — a Mac OS X CHM viewer
  * [KchmViewer](http://www.kchmviewer.net/) — a Qt/KDE based viewer of CHM files

# Links #

  * [HTML Help (CHM) Tools and Information](http://www.speakeasy.org/~russotto/chm/)
  * [Helpware](http://www.helpware.net/)
# About the GAR system #

The books are built using the [GAR system](http://www.lnx-bbc.com/garchitecture.html) -- a mechanism for automating the compilation and installation of third-party source code developed for the [LNX-BBC project](http://www.lnx-bbc.com/).

Here it is used to automate the download the sources, extract, patch, configure or build if necessary, and finally convert the documentation into the desired formats.

# Requirements #

To build all the books you will need:
  * A POSIX environment, such as [Linux](http://www.debian.org/) or [Cygwin](http://www.cygwin.com/).
  * [DocBook XSL and DSSSL Stylesheets](http://docbook.sourceforge.net/)
  * [xsltproc](http://xmlsoft.org/XSLT/)
  * [Doxygen](http://www.doxygen.org/)
  * [Microsoft HTML Help SDK](http://msdn.microsoft.com/library/en-us/htmlhelp/html/vsconHH1Start.asp) to build CHM.
  * [Wine](HHW4Wine.md) to run the Microsoft HTML Help compiler above, if not building under Windows.

# Download #

You can download the source from its [Subversion repository](http://htmlhelp.googlecode.com/svn/trunk/garbooks/):
```
svn co http://htmlhelp.googlecode.com/svn/trunk/garbooks/
```

# Usage #

  * Edit `htmlhelp.conf.mk` and choose the desired formats.
  * Run `make` in any directory, followed by one of the following targets:

| **Target** | **Description** |
|:-----------|:----------------|
| all | All formats |
| fetch | Download |
| garchive | Archive the downloads in ../garchive to prevent re-fetching them |
| chm | Create [CHM](CHM.md) books |
| devhelp | Create [DevHelp](DevHelp.md) books |
| htb | Create [HTB](HTB.md) books |
| clean | Clean all derivated files|
| makesums | Update the download checksums |
| bookarchive | Archive all generated books in ../books |
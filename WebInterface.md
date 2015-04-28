#summary Web Interface
#labels Tool

# Why a web interface? #

Using a web interfaces for a book repository has many advantages, such as platform independence and remote access. Since nowadays a web browser is mostly a commodity it becomes a privileged way to browse through a book collection.

# PHP Web Interface #

## About ##

This web interface stores all books in a MYSQL database and presents the books via PHP scripts

## Features ##

  * platform independent
  * blazing fast fulltext search with MySQL's FULLTEXT indexes
  * HTML rendering done by the web browser, which means that all HTML features are supported

## Requirements ##

Client requirements:

  * frame-capable web browser
  * a Gecko-based web browser with Javascript enabled for the XUL interface

Server requirements:

  * PHP 4
  * MYSQL
  * web server

## Live Demo ##

  * [htmlhelp.dotsrc.org](http://htmlhelp.dotsrc.org/) — still under construction

## Download ##

At the moment the source is only available from its [Subversion repository](http://htmlhelp.googlecode.com/svn/trunk/phphtmlhelp/).


# Links #

This is not an original concept. Open-source projects which also aim to present an interactive web interface to HTML reference documentation are:

  * [Linux Developer Network](http://lidn.sourceforge.net/) — a website service that offer programming function reference for the Linux/Gnome platform. It uses DevHelp scheme to show documents and the XML to index the documents.
  * [arCHMage](http://archmage.sourceforge.net/) — extensible online reader/decompiler of files in CHM format. It can be run as a standalone HTTP server or as an Apache `mod_python` handler.

Many projects have an interactive web interface for their own documentation. The norm is that the web interface is usually to specific to the documentation and the project needs. Nevertheless some have interesting ideas (such as user commenting and extensive searching) and are worth mention:

  * [PHP Online Documentation](http://www.php.net/manual/en/)
  * [MYSQL Online Documentation](http://www.mysql.com/doc/en/)

Another class is software which starts a local HTTP server to provide user documentation. Good examples are:

  * [Python](http://www.python.org/)'s `pydoc`
  * [Eclipse](http://www.eclise.org/)'s context help system
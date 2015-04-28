# Introduction #

pyhtmlhelp is a tool written in Python for converting among [CHM](CHM.md), [HTB](HTB.md), and [DevHelp](DevHelp.md) formats. Hopefully more formats will follow.

# Requirements #

  * [Python](http://www.python.org/) 2.3 or greater
  * [ctypes](http://cheeseshop.python.org/pypi/ctypes)
  * On Windows:
    * [comtypes](http://cheeseshop.python.org/pypi/comtypes) to read CHMs
    * [Microsoft HTML Help 1.3 SDK](http://msdn.microsoft.com/library/en-us/htmlhelp/html/vsconHH1Start.asp) to create CHMs
  * On Unix:
    * [CHMLIB](http://www.jedrea.com/chmlib/) to read CHMs
    * [Microsoft HTML Help 1.3 SDK and Wine](HHW4Wine.md) to write CHMs

# Usage #

Simply run:
```
  hhconvert.py <src-file> <dst-file>
```
to convert from src-file to dst-file. The formats will be guessed from the file
extensions.

## Supported formats ##

| **Format** | **Read** | **Write** | **Recognized extensions** |
|:-----------|:---------|:----------|:--------------------------|
| [CHM](CHM.md) | Yes | Yes | .chm |
| [DevHelp](DevHelp.md) | Yes | Yes | .tar, .tgz |
| [HTB](HTB.md) | Yes | Yes | .htb, .zip |
| [WinHelp](WinHelp.md) | No | No |  |

# Download #

  * [Latest release](http://htmlhelp.googlecode.com/files/pyhtmlhelp-0.5.tar.gz)
  * [Subversion repository](http://htmlhelp.googlecode.com/svn/trunk/pyhtmlhelp/)
```
svn co http://htmlhelp.googlecode.com/svn/trunk/pyhtmlhelp/
```
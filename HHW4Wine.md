# Requirements #

  * [Wine](http://www.winehq.org/)
    * It's assumed you have an empty Wine environment. Installed software in an existing Wine enviroment may cause conflicts during the installation steps below.
    * The following instructions were tested with **Wine version 0.9.47**. Your mileage with other versions will likely vary.
  * [cabextract](http://www.cabextract.org.uk/)

# Setup #

  1. Set Wine's Windows version to Windows 2000 (or above), and add an override to use the native `itss.dll`, both via `winecfg`:
```
wine winecfg
```
  1. Download [Microsoft HTML Help Workshop](http://msdn.microsoft.com/library/en-us/htmlhelp/html/hwMicrosoftHTMLHelpDownloads.asp) and  install it as:
```
wine htmlhelp.exe
```
  1. Install `itircl.dll` and `itss.dll` as:
```
cabextract -F hhupd.exe htmlhelp.exe
cabextract -F itircl.dll hhupd.exe
cabextract -F itss.dll hhupd.exe
cp -a itircl.dll ~/.wine/drive_c/windows/system32/
cp -a itss.dll ~/.wine/drive_c/windows/system32/
wine regsvr32 /s 'C:\WINDOWS\SYSTEM32\itircl.dll'
wine regsvr32 /s 'C:\WINDOWS\SYSTEM32\itss.dll'

```
  1. Download [Microsoft Foundation Classes update](http://activex.microsoft.com/controls/vc/mfc40.cab), extract it, and install it as:
```
wget http://activex.microsoft.com/controls/vc/mfc40.cab
cabextract mfc40.cab
wine mfc40.exe
wget -N http://activex.microsoft.com/controls/vc/mfc40.cab
cabextract -F mfc40.exe mfc40.cab
cabextract -F mfc40.dll mfc40.exe
cp -a mfc40.dll ~/.wine/drive_c/windows/system32/

```

Alternatively, download [htmlhelp.reg](http://htmlhelp.googlecode.com/svn/trunk/misc/htmlhelp.reg) and the [htmlhelp.sh](http://htmlhelp.googlecode.com/svn/trunk/misc/htmlhelp.sh) script, which will do all the work above for you.

# Usage #

You can now run the command line compiler by doing

```
wine 'C:\Program Files\HTML Help Workshop\hhc.exe' ...
```

You can now run the workshop by doing

```
wine 'C:\Program Files\HTML Help Workshop\hhw.exe' ...
```

# Links #

  * [IEs4Linux](http://www.tatanka.com.br/ies4linux/)
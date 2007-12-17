#!/bin/sh

# Setup the registry
wine regedit htmlhelp.reg

# Install HTML Help Workshop
wget -N 'http://go.microsoft.com/fwlink/?LinkId=14188'
WINEDLLOVERRIDES="advpack=n" wine htmlhelp.exe

# Install ITSS.DLL
cabextract -d htmlhelp htmlhelp.exe
cabextract -d hhupd hhupd.exe
cabextract -d hhupd htmlhelp/hhupd.exe
cp -a hhupd/itss.dll ~/.wine/drive_c/windows/system32/

# Install MFC40.DLL
wget -N http://download.microsoft.com/download/sql65/Patch/6.5/WIN98/EN-US/MFC40i.exe
cabextract -d MFC40i MFC40i.exe
cp -a MFC40i/mfc40.dll ~/.wine/drive_c/windows/system32/


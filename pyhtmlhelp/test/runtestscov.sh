#!/bin/sh

./coverage.py -e
./coverage.py -x runtests.py
echo
./coverage.py -r -m `find ../htmlhelp -iname '*.py'`

[ "$1" == "-a" ] && ./coverage.py -a `find ../htmlhelp -iname '*.py'`

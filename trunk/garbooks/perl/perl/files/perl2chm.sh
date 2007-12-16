#!/bin/sh

set -e 

OUTPUT="$1"

cd $OUTPUT

# Project file
exec 1>perl.hhp
cat << EOF
[OPTIONS]
Compiled file=perl.chm
Contents file=perl.hhc
Default Window=Main
Default topic=pod/perl.html
Full-text search=Yes
Index file=perl.hhk
Language=0x409 English (United States)
Title=Perl Documentation

[WINDOWS]
Main=,"perl.hhc","perl.hhk","pod/perl.html","pod/perl.html",,,,,0x22520,,0x384e,,,,,,,,0

[FILES]
EOF
find * -name '*.html'

# Contents file
exec 1>perl.hhc
echo '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">'
echo '<HTML>'
echo '<BODY>'
echo '<UL>'
echo "<LI> <OBJECT type=\"text/sitemap\"> <param name=\"Name\" value=\"PODs\"> </OBJECT>"
echo '<UL>'
find pod -maxdepth 1 -name '*.html' -printf '%p %f\n' | while read LINK NAME
do
	NAME=`echo $NAME | sed -e 's@\.html$@@'`
	echo "<LI> <OBJECT type=\"text/sitemap\"> <param name=\"Name\" value=\"$NAME\"> <param name=\"Local\" value=\"$LINK\"> </OBJECT>"
done
echo '</UL>'
echo "<LI> <OBJECT type=\"text/sitemap\"> <param name=\"Name\" value=\"Modules\"> </OBJECT>"
echo '<UL>'
find lib -name '*.html' -printf '%p %P\n' | while read LINK NAME
do
	NAME=`echo $NAME | sed -e 's@/@::@g' -e 's@\.html$@@'`
	echo "<LI> <OBJECT type=\"text/sitemap\"> <param name=\"Name\" value=\"$NAME\"> <param name=\"Local\" value=\"$LINK\"> </OBJECT>"
done
echo '</UL>'
echo '</UL>'
echo '</BODY>'
echo '</HTML>'

exec 1>perl.hhk
echo '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">'
echo '<HTML>'
echo '<BODY>'
echo '<UL>'
find pod -name '*.html' -printf '%p %f\n' | while read LINK NAME
do
	NAME=`echo $NAME | sed -e 's@\.html$@@'`
	echo "<LI> <OBJECT type=\"text/sitemap\"> <param name=\"Name\" value=\"$NAME\"> <param name=\"Local\" value=\"$LINK\"> </OBJECT>"
done
find lib -name '*.html' -printf '%p %P\n' | while read LINK NAME
do
	NAME=`echo $NAME | sed -e 's@/@::@g' -e 's@\.html$@@'`
	echo "<LI> <OBJECT type=\"text/sitemap\"> <param name=\"Name\" value=\"$NAME\"> <param name=\"Local\" value=\"$LINK\"> </OBJECT>"
done
echo '</UL>'
echo '</BODY>'
echo '</HTML>'

exec

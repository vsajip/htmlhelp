#!/usr/bin/perl

$texinfo = $ARGV[0];
$htmldir = $ARGV[1];

open(TEXINFO, "< $texinfo") || die;

open(HHP, "> $htmldir/gri.hhp") || die;
open(HHC, "> $htmldir/gri.hhc") || die;
open(HHK, "> $htmldir/gri.hhk") || die;

print HHP 
"[OPTIONS]
Compiled file=gri.chm
Contents file=gri.hhc
Default Window=Main
Default topic=index.html
Full-text search=Yes
Index file=gri.hhk
Language=0x409 English (United States)
Title=Gri

[WINDOWS]
Main=,\"gri.hhc\",\"gri.hhk\",\"index.html\",\"index.html\",,,,,0x22520,,0x384e,,,,,,,,0

[FILES]
index.html
";


print HHC
"<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML//EN\">
<HTML>
<BODY>
";

print HHK
"<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML//EN\">
<HTML>
<BODY>
<UL>
";

while(<TEXINFO>) {

	if (/^\@c\s*HTML\s*<!--\s*$/) {
		while(<TEXINFO>) {
			if (/^\@c\s*HTML\s*-->\s*$/) {
				last;
			}
		}
		<TEXINFO>;
	}
	
	if (/^\@c\s*HTML\s*<!-- newfile\s+([^ ]*)\s+"(.*)"\s+"(.*)"\s*-->\s*$/) {
		$filename = $1;
		$title = $2;

		print HHP $filename . "\n";
	}

	s/\@code{([^}]*)}/$1/g;
	s/\@uref{[^,]*,([^}]*)}/$1/g;
	s/\@\@/@/g;

	s/&/&amp;/g;
	s/</&lt;/g;
	s/>/&gt;/g;
	s/'/&apos;/g;
	s/"/&quot;/g;

	if (/^\@node\s*([^,]*), ([^,]*), ([^,]*), ([^\n]*)/o) {
		$anchor = $1;
		$anchor =~ s/ //g;
		$link = "$filename#$anchor";
	}

	if (/\@chapter/o
		|| /\@section/o
		|| /\@subsection/o
		|| /\@subsubsection/o
		|| /\@subsubsubsection/o
		|| /\@unnumbered/o
		|| /\@appendixsubsec/o
		|| /\@appendixsec/o
		|| /\@appendix/o) {
		
		if (/\@chapter\s*(.*)/) {
			$CH++;
			$SEC1 = 0;
			$level = 1;
			$name = "$CH: $1";

		} elsif (/\@unnumbered\s*(.*)/) {
			$CH++;
			$SEC1 = 0;
			$level = 1;
			$name = "$CH: $1";
		} elsif (/\@section\s*(.*)/) {
			$SEC1++;
			$SEC2 = 0;
			$level = 2;
			$name = "$CH.$SEC1: $1";
		} elsif (/\@subsection\s*(.*)/) {
			$SEC2++;
			$SEC3 = 0;
			$level = 3;
			$name = "$CH.$SEC1.$SEC2: $1";
		} elsif (/\@subsubsection\s*(.*)/) { 
			$SEC3++;
			$level = 4;
			$name = "$CH.$SEC1.$SEC2.$SEC3: $1";
		}

		while ($curlevel < $level) {
			print HHC "<UL>\n";
			$curlevel++;
		}
		while ($curlevel > $level) {
			print HHC "</UL>\n";
			$curlevel--;
		}
				

		print HHC "<LI> <OBJECT type=\"text/sitemap\"> <param name=\"Name\" value=\"$name\"> <param name=\"Local\" value=\"$link\"> </OBJECT>\n";
	}
	
	if(/\@[cfv]index\s*(.*)/) {
		$name = $1;
		print HHK "<LI> <OBJECT type=\"text/sitemap\"> <param name=\"Name\" value=\"$name\"> <param name=\"Local\" value=\"$link\"> </OBJECT>\n";
	}
}

while ($curlevel > 0) {
	print HHC "</UL>\n";
	$curlevel--;
}

print HHC
"</BODY>
</HTML>
";

print HHK
"</UL>
</BODY>
</HTML>
";

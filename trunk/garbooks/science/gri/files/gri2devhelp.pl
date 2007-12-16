#!/usr/bin/perl

$texinfo = $ARGV[0];

print "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"no\"?>\n";
print "<book title=\"The Gri Graphing Languange\" name=\"gri\" link=\"index.html\">\n";

print "\t<chapters>\n";
open(TEXINFO, "< $texinfo") || die;
$curlevel = 1;
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
			print "<sub name=\"\">\n";
			$curlevel++;
		}
		while ($curlevel > $level) {
			print "</sub>\n";
			$curlevel--;
		}
				

		print "<sub name=\"$name\" link=\"$link\">\n";
		$curlevel++;
	}
}
while ($curlevel > 1) {
	print "</sub>\n";
	$curlevel--;
}
close TEXINFO;
print "\t</chapters>\n";

print "\t<functions>\n";
open(TEXINFO, "< $texinfo") || die;
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

	if(/\@[cfv]index\s*(.*)/) {
		$name = $1;
		print "\t\t<function name=\"$name\" link=\"$link\"/>\n";
	}
}
close TEXINFO;
print "\t</functions>\n";

print "</book>\n";

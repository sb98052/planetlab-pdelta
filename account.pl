#!/usr/bin/perl
# Generate XML file for Node graph, and other daily statistics

$accountdir="/usr/local/pdelta-production-4.0/accounting";

@ar=localtime;
system("echo ".$ar[2].$ar[1].$ar[0].">/tmp/lastaccount");
$fname="nodecount-".($ar[5]+1900)."-".($ar[4]+1)."-".$ar[3];

open FIL,"$accountdir/$fname" || exit(0);

open W,">/var/www/html/graph.xml";
print W "<?xml version=\"1.0\" encoding=\"utf-8\"?>";
print W "<graph line_color=\"0xff9900\">";

while (<FIL>) {
	if (/(.+) (\d+)/) {
		print W "<data label=\"$1\" value=\"$2\" />"			
	}
}

print W "</graph>";
close W;
close FIL;

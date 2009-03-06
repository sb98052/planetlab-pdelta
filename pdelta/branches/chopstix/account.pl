#!/usr/bin/perl
# Daily accounting script for a PlanetFlow Central installation.
# Stores PlanetFlow's nodecounts in timestamped XML files

$accountdir="/usr/local/pdelta-production-4.0/accounting";

@ar=localtime;
@ar2=localtime(time()-86400);

$fname="nodecount-".($ar[5]+1900)."-".($ar[4]+1)."-".$ar[3];
$fname2="nodecount-".($ar2[5]+1900)."-".($ar2[4]+1)."-".$ar2[3];

open FIL,"$accountdir/$fname" || exit(0);
open FIL2,"$accountdir/$fname2"; 

open W,">/var/www/html/graph.xml";
print W "<?xml version=\"1.0\" encoding=\"utf-8\"?>";
print W "<graph line_color=\"0xff9900\">";

$hours=$ar[2];

while (<FIL2>) {
	if (/(.+) (\d+)/) {
 	    if (int($1) > $hours ) {
		print W "<data label=\"$1\" value=\"$2\" />"			
	    }		
	}
}

while (<FIL>) {
	if (/(.+) (\d+)/) {
		print W "<data label=\"$1\" value=\"$2\" />"			
	}
}

print W "</graph>";
close W;
close FIL;
close FIL2;

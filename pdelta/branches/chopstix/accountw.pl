#!/usr/bin/perl
# Weekly accounting script for a PlanetFlow installation

$accountdir="/usr/local/pdelta-production-4.0/accounting";

open W,">/var/www/html/graphw.xml";
print W "<?xml version=\"1.0\" encoding=\"utf-8\"?>";
print W "<graph line_color=\"0xff9900\">";

foreach $days (0..6) {
	my $daycount;
	my $daysum;	
	$daycount=0;
	$daysum=0;
	$back=6-$days;
	
	@ar=localtime(time()-(86400*$back));
	$year=$ar[5]+1900;
	$mon=$ar[4]+1;
	$day=$ar[3];
	$fname="$accountdir/nodecount-".$year."-".$mon."-".$day;

	open FIL,$fname || next;

	while (<FIL>) {
		if (/(.+) (\d+)/) {
			$daycount=$daycount+1;
			$daysum=$daysum+int($2);
		}
	}

	if ($daycount==0) { next;}
	$avg=int($daysum/$daycount);

	print W "<data label=\"$year/$mon/$day\" value=\"$avg\"/>";
	close FIL;

	
}
print W "</graph>";
close W;

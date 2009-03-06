#!/usr/bin/perl

open C,$ARGV[0];
@res=<C>;
close C;

shift @res;
for (@res) {
	s/\s//g;
	if (m/(\d+)\|(\d+)\|(\d+)\|(\d+)/) {
		$packets=int($4);
		$bytes=int($3);
		$totalbytes+=$bytes;
		$totalpackets+=$packets;
	}
}


sub commify {
    local($_) = shift;
    1 while s/^(-?\d+)(\d{3})/$1,$2/;
    return $_;
} 

$path="/usr/local/pdelta-production-4.0/trunk/data/";
$maxp=`cat $path/max_packets`;
$avgp=`cat $path/avg_packets`;
$maxd=`cat $path/max_data`;
$avgd=`cat $path/avg_data`;

if ($maxp==0 || int($maxp)>$totalpackets) {
	system("echo $totalpackets > $path/max_packets");
	if ($maxp==0) {
		$maxp=$totalpackets;
	}
}

if ($maxd==0 || int($maxb)>$totalbytes) {
	system("echo $totalbytes > $path/max_data");
	if ($maxd==0) {
		$maxd=$totalbytes;
	}
}

$maxpfrac=$totalpackets/int($maxp);
$maxdfrac=$totalbytes/int($maxd);

$maxpfrac*=100;
$maxdfrac*=100;

$numslices=$#res;

print "<p>Yesterday, <big>".commify($totalpackets)."</big> packets were transmitted by PlanetLab hosts. This is <big>$maxpfrac%</big> of the maximum 
transmission I have seen. In terms of bytes, a total of <big>".commify($totalbytes)."</big> were transmitted, which is <big>$maxdfrac%</big> of the maxium transmission that I have seen.</p>";
print "<p>A total of <big>$numslices</big> slices participated in this transmission.</p>";

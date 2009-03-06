#!/usr/bin/perl

$rawdir="/usr/local/pdelta-production-4.0/data_raw";
$importdir="/usr/local/pdelta-production-4.0/data_import";
$silkdir="/usr/local/pdelta-production-4.0/local/sbin";

system("find $rawdir -name \"pf*\" -size +0 -mtime -2 > /tmp/to_harvest");

open FIL,"/tmp/to_harvest";

while (<FIL>) {
	if (/(\d+\.\d+\.\d+\.\d+)\/(pf2\.\d+)/) {
		$rawf="$1/$2";
		$import_cmd = "$silkdir/rwflowpack --input-mode=file --netflow-file=$rawdir/$1/$2 --sensor-configuration=$rawdir/$1/sensor.conf --root-directory=$importdir --log-destination=none --site-config-file=silk.conf";
		print "Executing $import_cmd\n"; 
		@ar=stat "$rawdir/$rawf";
		$mtime=$ar[9];
		system($import_cmd);
		open W,">$rawdir/$rawf";
		truncate(W,0);
		close W;
		utime $mtime,$mtime,"$rawdir/$rawf";
	}
}

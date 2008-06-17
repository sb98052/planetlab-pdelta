# Harvest.pl
# Run this before restarting pdelta
#
#!/usr/bin/perl

$days=2; # When did pdelta crash?

$rawdir="/usr/local/pdelta-production-4.0/data_raw";
$importdir="/usr/local/pdelta-production-4.0/data_import";

system("find $rawdir -name \"pf*\" -size +0 -mtime -$days > /tmp/to_harvest");

open FIL,"/tmp/to_harvest";

while (<FIL>) {
	if (/(\d+\.\d+\.\d+\.\d+)\/(pf2\.\d+)/) {
		$rawf=$1;
		$import_cmd = "/usr/local/pdelta-production-4.0/local/sbin/rwflowpack --input-mode=file --netflow-file=$rawdir/$1/$2 --sensor-configuration=$rawdir/$1/sensor.conf --root-directory=$importdir --log-destination=none --site-config-file=silk.conf";
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

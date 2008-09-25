#!/usr/bin/perl

my $path='/usr/local/pdelta-production-4.0';
my $tpath='/usr/local/pdelta-production-4.0/trunk';
my $statspath='/usr/local/pdelta-production-4.0/trunk/data';
my $binpath=$path."/local/bin";
my $datapath=$path."/data_import";
my $silkpath=$path."/trunk/silk.conf";
my $htmlpath="/var/www/html";

my @today;
my $cmd;

@today=localtime;
$today[5]+=1900;
$today[4]+=1;
 
$cmd="$binpath/rwfilter --pass-destination stdout --type=all --data-rootdir $datapath --site-config-file $silkpath --start-date ".$today[5]."/".$today[4]."/".$today[3]." --end-date ".$today[5]."/".$today[4]."/".$today[3]." --slice 0- | $binpath/rwuniq --fields=slice --packet --bytes";

$statsfile="$statspath/traffic-".$today[5]."-".$today[4]."-".($today[3]-1);
system("$cmd > $statsfile");

$cmd="$tpath/agg-traffic.pl $statsfile > $htmlpath/traffic.html";
print $cmd."\n";
system("$cmd");

$cmd="$tpath/slice-traffic.pl $statsfile > $htmlpath/slices.html";
print $cmd."\n";
system("$cmd");

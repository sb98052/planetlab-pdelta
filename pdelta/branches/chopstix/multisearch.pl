#!/usr/bin/perl

open G, $ARGV[0];
@g=<G>;
close G;

foreach $ip (@g) {
	chomp($ip);
	$cmd='/usr/local/pdelta-production-4.0/local/bin/rwfilter --pass-destination stdout --type=all --data-rootdir /usr/local/pdelta-production-4.0/data_import/ --site-config-file /usr/local/pdelta-production-4.0/trunk/silk.conf --sensor S'.$ip.' --start-date 2008/7/11 --end-date 2008/7/18 --xid 16203 --dport 2706'.$ip.' | /usr/local/pdelta-production-4.0/rwcut ';
	system($cmd);
}

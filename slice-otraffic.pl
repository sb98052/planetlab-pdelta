#!/usr/bin/perl

open C,$ARGV[0];
@res=<C>;
close C;

shift @res;
for (@res) {
	s/\s//g;
	if (m/(\d+)\|(\d+)\|(\d+)\|(\d+)/) {
		$hash{$1}=int($4);
		$hash2{$1}=int($3);
	}
}

@sorted = sort { $hash{$b} <=> $hash{$a} } keys %hash; 
@sorted2 = sort { $hash2{$b} <=> $hash2{$a} } keys %hash; 

sub commify {
    local($_) = shift;
    1 while s/^(-?\d+)(\d{3})/$1,$2/;
    return $_;
}

$path="/usr/local/pdelta-production-4.0/trunk";

print '<td>';
print '<h3 style="text-align:center;align:center">Slices transmitting the most OOPL packets</h3>';
print '<p style="text-align:center;align:center">Go <b>'.`$path/fast_get_slices.py $sorted[1]`.'!</b></p>';

print '<table border="1" padding="0" style="margin-left:auto;margin-right:auto">';
print '<tr><td>Slice</td><td>Packets</td></tr>';	
foreach (@sorted[0..10]) {
	if ($_ eq "0") {
		next;
	}
	print "<tr>";
	print "<td>".`$path/fast_get_slices.py $_`."</td>";
	print "<td>".commify(int($hash{$_}))."</td>";
	print "</tr>";	
}
print '</td></tr>';
print '</table>';
print '</td><td>';
print '<table>';
print '<h3 style="text-align:center;align:center">Slices transmitting the most OOPL data</h3>';
print '<p style="text-align:center;align:center">Go <b>'.`$path/fast_get_slices.py $sorted2[1]`.'!</b></p>';
print '<table border="1" padding="0" style="margin-left:auto;margin-right:auto">';
print '<tr><td>Slice</td><td>Bytes</td></tr>';	

foreach (@sorted2[1..10]) {
	print "<tr>";
	print "<td>".`$path/fast_get_slices.py $_`."</td>";
	print "<td>".commify(int($hash2{$_}))."</td>";
	print "</tr>";	
}
print '</table>';
print '</td>';

#!/usr/bin/python

max_bandwidth = 10 					# in megaoctects/second. b/w cap on PFC
wait_between_spawns = 10			# number of seconds to wait between rsync session spawns.
slice_name = "pl_netflow"
path = "/pf"
#plcapi = "https://www.planet-lab.org/PLCAPI/"
plcapi = "https://pl-virtual-06.cs.princeton.edu/PLCAPI/"
tmpdir = "."
do_bw_limit = False

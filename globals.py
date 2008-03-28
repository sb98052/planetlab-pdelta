#!/usr/bin/python

max_bandwidth = 10 					# in megaoctects/second. b/w cap on PFC
wait_between_spawns = 10			# number of seconds to wait between rsync session spawns.
#slice_name = "pl_netflow"
#path = "/pf"
#plcapi = "https://pl-virtual-06.cs.princeton.edu/PLCAPI/"
#tmpdir = "."
slice_name = "root"
path = "/usr/local/fprobe"
plcapi = "https://boot.planet-lab.org/PLCAPI/"
rawdatadir = "/usr/local/pdelta-testing/data_raw"
silkdatadir= "/usr/local/pdelta-testing/data_import"
tmpdir = rawdatadir
do_bw_limit = False

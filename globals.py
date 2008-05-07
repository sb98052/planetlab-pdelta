#!/usr/bin/python

do_bw_limit = False
max_bandwidth = 10                                      # in megaoctects/second. b/w cap on PFC
wait_between_spawns = 10                        # number of seconds to wait between rsync session spawns.
slice_name = "root"

paths = [ "/usr/local/fprobe", "/var/local/fprobe" ]
plcapi = "https://boot.planet-lab.org/PLCAPI/"
silkpath = "/usr/local/pdelta-production-4.2/local/"
rawdatadir = "/usr/local/pdelta-production-4.2/data_raw"
silkdatadir= "/usr/local/pdelta-production-4.2/data_import"

# You may set one, the other, or neither.  But, not both.
nodegroup_exclude = None
nodegroup = 'Alpha'

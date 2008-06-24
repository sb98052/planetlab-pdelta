#!/usr/bin/python

do_bw_limit = False
max_bandwidth = 10                                        # in megaoctects/second. b/w cap on PFC
max_concurrency = 2                                       # in megaoctects/second. b/w cap on PFC
wait_between_spawns = 10                        # number of seconds to wait between rsync session spawns.
slice_name = "root"
concurrency = 0
starttime = 0.0

node_count = 0
accountdir="."
paths = [ "/var/local/fprobe" ]
plcapi = "https://boot.planet-lab.org/PLCAPI/"
silkpath = "/usr/local/pdelta-production-4.0/local/"
rawdatadir = "/usr/local/pdelta-production-4.0/data_raw"
silkdatadir= "/usr/local/pdelta-production-4.0/data_import"

# You may set one, the other, or neither.  But, not both.
nodegroup_exclude = None
nodegroup = None

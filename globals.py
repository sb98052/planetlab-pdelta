#!/usr/bin/python

import re

plprefix='pl'
# plprefix='ple'

do_bw_limit = False
max_bandwidth = 10                                        # in megaoctects/second. b/w cap on PFC
max_concurrency = 13                                       # in megaoctects/second. b/w cap on PFC
wait_between_spawns = 10                        # number of seconds to wait between rsync session spawns.
concurrency = 0
starttime = 0.0

node_count_prod = 0
node_count_deb = 0
accountdir="/usr/local/cdelta-production-4.0/accounting"
paths = ["/var/local/chopstix","/tmp/mnt/sysimg/vservers/princeton_chopstix/var/local/chopstix" ]
debug_mask = re.compile(r'^/tmp/mnt/sysimg')


plcaccess = [("https://boot.planet-lab.org/PLCAPI/","pl",dict(AuthMethod='password',Username='sapanb@cs.princeton.edu',AuthString='')),("https://boot.planet-lab.eu/PLCAPI/","ple",dict(AuthMethod='anonymous'))]
#silkpath = "/usr/local/pdelta-production-4.0/local/"
rawdatadir = "/d/data/chopstix"
#silkdatadir= "/usr/local/pdelta-production-4.0/data_import"

# You may set one, the other, or neither.  But, not both.
nodegroup_exclude = None
nodegroup = 'chopstix'

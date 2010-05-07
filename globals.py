#!/usr/bin/python

import re

# PFC-specific variables
# If you are bringing up your own PFC, then you should only
# need to configure the variables below

# Change the following to the prefix you set when you ran
# plc-tty-config
plprefix='pl'

# 'accountdir' points to a directory that pdelta uses to dump statistics
# about the data collected. As long as you set this to a directory writable by pdelta, you should be fine
accountdir="/usr/local/pdelta-production-4.0/accounting"

# The following is a 'last-resort' hack for dealing with situations in which 
# the planetflow slice is not set up properly on a node. If you think your plprefix_netflow slice is guaranteed to be set up properly, then feel free to set the following to an empty dict

path_hook = { "/pf":"if [ ! -e /etc/init.d/pf2slice ]; then wget www.cs.princeton.edu/~sapanb/pf2slice;sudo mkdir -p /pf;sudo mv pf2slice /etc/init.d;sudo chmod +x /etc/init.d/pf2slice;sudo /sbin/chkconfig --add pf2slice;sudo /sbin/service pf2slice start; fi" }
# path_hook = {}

# List of PLCs you would like to gather data from, with the authentication tokens set 
plcaccess = [("https://boot.planet-lab.org/PLCAPI/","pl",dict(AuthMethod='password',Username='gwsapan@gmail.com',AuthString='')),("https://www.planet-lab.eu/PLCAPI/","ple",dict(AuthMethod='anonymous'))]

# Silk directories. For pdelta to work, just make sure that these are writeable.
silkpath = "/usr/local/pdelta-production-4.0/local/"
rawdatadir = "/usr/local/pdelta-production-4.0/data_raw"
silkdatadir= "/usr/local/pdelta-production-4.0/data_import"


###
###
###
### Advanced - please read the source code before modifying these


debug_mask = re.compile(r'^/tmp/mnt/sysimg')
paths = [ "/pf","/tmp/mnt/sysimg/var/local/fprobe","/var/local/fprobe" ]
do_bw_limit = False
max_bandwidth = 10                                        # in megaoctects/second. b/w cap on PFC
max_concurrency = 13                                       # in megaoctects/second. b/w cap on PFC
wait_between_spawns = 10                        # number of seconds to wait between rsync session spawns.
concurrency = 0
starttime = 0.0

node_count_prod = 0
node_count_deb = 0

# You may set one, the other, or neither.  But, not both.
nodegroup_exclude = None
nodegroup = None

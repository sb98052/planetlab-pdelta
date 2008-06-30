#!/usr/bin/python

import globals
import time

def log_node_count (production,debug):
	curtime=time.localtime()
	acfile="%s/nodecount-%d-%d-%d"%(globals.accountdir,curtime[0],curtime[1],curtime[2])
	FILE = open(acfile,"a")
	FILE.write("%02d:%02d %d\n" % (curtime[3],curtime[4],production))
	FILE.close()

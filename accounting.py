#!/usr/bin/python

import globals
import time

def log_node_count (count):
	acfile="%s/%s"%(globals.accountdir,"ac")
	curtime=time.localtime()
	FILE = open(acfile,"a")
	FILE.write("%d/%d/%d %2d:%2d -> %d\n" % (curtime[0],curtime[1],curtime[2],curtime[3],curtime[4],count))
	FILE.close()


#!/usr/bin/python
# We populate 3 lists - green is the lowest priority list, which is the output of getnodes()
# blue is the mid-priority list. Every time there's  

import os
import logger
import accounting
import globals
import time

from sets import Set
import getnodes

green = []
blue = []
red = []

redset = Set(red)
blueset = Set(blue)

def reinit ():
	global greeniter
	nodes = getnodes.file_get_node_list(['hostname', 'node_id'], 'green')
	greeniter = iter(nodes)

def get_next_pending ():
	# Check in the following order: red, blue, green
	global redset
	global blueset

	if (os.path.exists("red")):
		try:
			f = open("red")
			to_append = filter(lambda x: x in redset,f.readlines())   
			red.extend(to_append)
			f.close ()
			posix.unlink("red")
		except OSError:
			a=1
	if (os.path.exists("blue")):
		try:
			f = open ("blue")
			to_append = filter (lambda x: x in blueset,f.readlines())
			blue.extend (to_append)
			f.close ()
			posix.unlink("blue")
		except OSError:
			a=1

	if (len(red) != 0):
		ret = red.pop()
		redset = Set(red)
	else:
		if (len(blue) != 0):
			ret = blue.pop()
			blueset = Set(blue)
		else:
			global greeniter

			newiteration = 0
			try:
				next = greeniter.next()
			except StopIteration:
				newiteration = 1

			if (newiteration):
				while (globals.concurrency > globals.max_concurrency):
					print("Waiting for lingering processes to complete..")
					print("Concurrency=%d"%(globals.concurrency))
					sleep(60)

				accounting.log_node_count(globals.node_count_prod,globals.node_count_deb)
				globals.node_count_deb = 0
				globals.node_count_prod = 0
				logger.l.debug("reloading: 'green' list")

				duration = time.time() - globals.start_time
				if (duration < 3600):
					margin = 3600 - duration
					print("Finished the last run in %f seconds. Sleeping for %f seconds"%(duration,margin+300))
					time.sleep(3600)
					print("Waking up...")
					print("Concurrency=%d"%(globals.concurrency))
					globals.start_time = time.time()
		
				green_list = getnodes.file_get_node_list(['hostname', 'node_id'], 'green')
				greeniter = iter(green_list)
				next = greeniter.next()

			ret = (next[0],next[1].rstrip())
	return ret

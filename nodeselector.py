#!/usr/bin/python
# We populate 3 lists - green is the lowest priority list, which is the output of getnodes()
# blue is the mid-priority list. Every time there's  

import os
import logger

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
			try:
				next = greeniter.next()
			except StopIteration:
				print "got StopIteration..."
				logger.l.debug("reloading: 'green' list")
				green_list = getnodes.file_get_node_list(['hostname', 'node_id'], 'green')
				greeniter = iter(green_list)
				next = greeniter.next()
			ret = next.rstrip()
	return ret

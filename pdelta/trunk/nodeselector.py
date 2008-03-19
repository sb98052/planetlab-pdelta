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

def getListFromFile(file):
    f = open(file, 'r')
    list = []
    for line in f:
        line = line.strip()
        list += [line]
    return list

def reinit ():
	if not os.path.exists("green"):
		logger.l.debug("Creating 'green' file")
		nodes = getnodes.get_node_list()
		f = open("green", 'w')
		for n in nodes:
			logger.l.debug("saving: %s" % n)
			print >>f, "%s\n" % n
		f.close()

	# Read the green list
	if (os.path.exists("green")):
		try:
			global greeniter
			logger.l.debug("loading: 'green' file")
			green_list = getListFromFile("green")
			greeniter = iter(green_list)

		except OSError:
			logger.log( "green: file not found.")

def get_next_pending ():
	# Check in the following order: red, blue, green
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
			print "getting next host"
			try:
				next = greeniter.next()
			except StopIteration:
				print "got StopIteration..."
				logger.l.debug("loading: 'green' file")
				green_list = getListFromFile("green")
				greeniter = iter(green_list)
				next = greeniter.next()
			ret = next.rstrip()
	return ret

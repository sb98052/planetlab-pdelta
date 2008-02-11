#!/usr/bin/python
# We populate 3 lists - green is the lowest priority list, which is the output of getnodes()
# blue is the mid-priority list. Every time there's  

import os
import logger

from sets import Set

green = []
blue = []
red = []

redset = Set(red)
blueset = Set(blue)

greeniter = iter(green)

def reinit ():
		# Read the green list
		if (os.path.exists("green")):
				try:
						f = open("green")
						green = f.readlines()
						greeniter = iter(green)

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
				if (len(red) != 0):
						ret = red.pop()
						redset = Set(red)
				else:
						try:
								f = open ("blue")
								to_append = filter (lambda x: x in blueset,f.readlines())
								blue.extend (to_append)
								f.close ()
								posix.unlink("blue")
						except OSError:
							a=1

						if (len(blue) != 0):
								ret = blue.pop()
								blueset = Set(blue)
						else:
								ret = greeniter.next()
				

	



		
















#!/usr/bin/python

import os
import sys
import globals
import getnodes

def writeDataToFile(data, file):
    f = open(file, 'w')
    f.write(data)
    f.close()

# expects nodes to be a list of ip,node_id tuples, returned from raw_get_node_list()
def create_silkconf(nodes):

	if not os.path.exists(globals.rawdatadir): os.mkdir(globals.rawdatadir)
	if not os.path.exists(globals.silkdatadir): os.mkdir(globals.silkdatadir)
		
	i = 0
	sensorlist = []
	curips = {}
	sf = open('silk.conf.tmp', 'w')
	for ip,id in nodes:
		if (not curips.ContainsKey(ip)):
			print >>sf, "sensor %s S%s" % (id, ip )
			sensorlist.append("S%s" % ip)
			curips[ip]=True
		data="""
	sensor-probe  S%s
		probe-name netflow                # optional but recommended
		probe-type netflow                # default value
		priority 8                        # optional
		external-ipblock remainder
		internal-ipblock %s
		read-from-file /dev/null
		""" % (ip, ip)
		path = "%s/%s" % (globals.rawdatadir,ip)
		if not os.path.exists(path): os.mkdir(path)
		sensorfile_tmp = "%s/%s/sensor.conf.tmp" % (globals.rawdatadir, ip)
		sensorfile     = "%s/%s/sensor.conf" % (globals.rawdatadir, ip)
		writeDataToFile(data, sensorfile_tmp)
		os.rename(sensorfile_tmp, sensorfile)

	print >>sf, "class all"
	print >>sf, "    sensors", " ".join(sensorlist)
	print >>sf, "end class"

	print >>sf, "version 1"

	print >>sf, """
	class all
		type  0 in      in
		type  1 out     out
		type  2 inweb   iw
		type  3 outweb  ow
		type  4 innull  innull
		type  5 outnull outnull
		type  6 int2int int2int
		type  7 ext2ext ext2ext
		type  8 inicmp  inicmp
		type  9 outicmp outicmp
		type 10 other   other

		default-types in inweb inicmp
	end class

	default-class all
	"""
	sf.close()
	os.rename("silk.conf.tmp", "silk.conf")

if __name__ == "__main__":
	nodes = getnodes.raw_get_node_list(['hostname', 'node_id'])
	create_silkconf(nodes)

#!/usr/bin/python

import os
import sys
import globals
import getnodes

def getListFromFile(file):
    f = open(file, 'r')
    list = []
    for line in f:
        line = line.strip()
        list += [line]
    return list

def writeDataToFile(data, file):
    f = open(file, 'w')
    f.write(data)
    f.close()

nodes = getnodes.get_node_list(['hostname', 'node_id'])
f = open("green", 'w')
for ip,id in nodes:
    print >>f, "%s" % ip
f.close()

filelist = getListFromFile("green")
if not os.path.exists(globals.tmpdir): os.mkdir(globals.tmpdir)
    
i = 0
sensorlist = []
sf = open('silk.conf', 'w')
for ip,id in nodes:
    print >>sf, "sensor %s S%s" % (id, ip )
    sensorlist.append("S%s" % ip)
    
    data="""
sensor-probe  S%s
    probe-name netflow                # optional but recommended
    probe-type netflow                # default value
    priority 8                        # optional
    external-ipblock remainder
    internal-ipblock %s
    read-from-file /dev/null
    """ % (ip, ip)
    path = "%s/%s" % (globals.tmpdir,ip)
    if not os.path.exists(path): os.mkdir(path)
    writeDataToFile(data, "%s/%s/sensor.conf" % (globals.tmpdir, ip))

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

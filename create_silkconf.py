#!/usr/bin/python

import sys

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

filelist = getListFromFile(sys.argv[1])
i = 0
sensorlist = []
for file in filelist:
    print "sensor %s S%s" % (i, file)
    i = i+1
    sensorlist.append("S%s" % file)
    
    data="""
sensor-probe  S%s
    probe-name netflow                # optional but recommended
    probe-type netflow                # default value
    priority 8                        # optional
    external-ipblock remainder
    internal-ipblock %s
    read-from-file /dev/null
	""" % (file, file)
    writeDataToFile(data, "data/%s/sensor.conf" % file)

print "class all"
print "    sensors", " ".join(sensorlist)
print "end class"

print "version 1"

print """
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

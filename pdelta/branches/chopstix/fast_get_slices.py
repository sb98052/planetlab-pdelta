#!/usr/bin/python

import xmlrpclib
import sys
import MySQLdb

def format(slicename):
	return (slicename)

if __name__ == "__main__":
	sliceid=int(sys.argv[1])
	conn = MySQLdb.connect (host = "localhost",
				user = "root",
				passwd = "foobar",
				db = "planetflow")

	cursor = conn.cursor ()
	cursor.execute ("SELECT name FROM slices WHERE id=%s" % sys.argv[1])
	row = cursor.fetchone ()
	if ( sliceid==0 ):
		link = format('root')
	elif ( not row ):
		plcapi = "https://boot.planet-lab.org/PLCAPI/"
		s = xmlrpclib.ServerProxy(plcapi, allow_none=True)
		auth = dict(AuthMethod='password',Username='sapanb@cs.princeton.edu',AuthString='')
		
		slices=s.GetSlices(auth,{'slice_id':sliceid})
		if (len(slices)>0):
			sliceid_str="%s"%sliceid
			slicename=slices[0]['name']
			insertcmd='INSERT INTO slices (id,name,descr) VALUES (%s,\'%s\',\'%s\')'%(sliceid_str,slicename,'')
			cursor.execute(insertcmd)
			link = format(slices[0]['name'])
		else: 
			link = "Id %d" % sliceid
	else:
		link = format(row[0])
		
	print link


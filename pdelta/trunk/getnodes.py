#!/usr/bin/python

import socket
import xmlrpclib

def get_node_list ():
		ret = []
		s = xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/')
		nodes = s.GetNodes(dict(AuthMethod='anonymous'), {}, ['hostname'])
		for node in nodes:
		   try:
			    print socket.gethostbyname(node['hostname'])
		   except socket.gaierror:
			   pass

get_node_list ()

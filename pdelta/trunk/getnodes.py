#!/usr/bin/python

import socket
import xmlrpclib
import globals
import logger

def get_node_list ():
	
	logger.l.debug("Entered get_node_list")
	ret = []
	s = xmlrpclib.ServerProxy(globals.plcapi)
	nodes = s.GetNodes(dict(AuthMethod='anonymous'), {}, ['hostname'])
	for node in nodes:
		try:
			ip = socket.gethostbyname(node['hostname'])
			ret.append(ip)
		except socket.gaierror:
			pass
	return ret

if __name__ == "__main__":
	get_node_list ()

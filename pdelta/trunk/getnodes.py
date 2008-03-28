#!/usr/bin/python

import socket
import xmlrpclib
import globals
import logger

def get_node_list (filter=['hostname']):
	
	logger.l.debug("Entered get_node_list")
	ret = []
	s = xmlrpclib.ServerProxy(globals.plcapi)
	nodes = s.GetNodes(dict(AuthMethod='anonymous'), {}, filter)
	for node in nodes:
		try:
			ip = socket.gethostbyname(node['hostname'])
			if 'node_id' in filter:
				ret.append((ip,node['node_id']))
			else:
				ret.append(ip)
		except socket.gaierror:
			pass
	return ret

if __name__ == "__main__":
	get_node_list ()

#!/usr/bin/python

import socket
import xmlrpclib
import globals
import logger
import create_silkconf
import os

from sets import Set

def getListFromFile(file):
    f = open(file, 'r')
    list = []
    for line in f:
        line = line.strip()
        list += [line]
    return list

def setFileFromList(list,file):
	f = open(file, 'w')
	for n in list:
		print >>f, "%s" % n
	f.close()

def file_get_node_list(filter=['hostname'], file='green'):
	nodes = []

	try:
		allnodes = raw_get_node_list(filter)
		for (pref, lst) in allnodes:
				nodes.extend(lst)
					
		if 'node_id' in filter:
			create_silkconf.create_silkconf(nodes)
			nodes = [ n[0] for n in nodes ]
		logger.l.debug("Creating '%s' file", file)
		setFileFromList(nodes, file)
	except OSError:
		logger.log("%s: could not write to file." % file)
		logger.log("Should not continue without backup node list.")
		sys.exit(1)
	except:
		import traceback
		print traceback.prine_exc()
			
		# api error, or other.
		# Read the node list
		if (os.path.exists(file)):
			try:
				nodes = getListFromFile(file)
			except OSError:
				logger.log("%s: file not found." % file)
				logger.log("Cannot continue without node list.")
				sys.exit(1)

	return nodes

def raw_get_node_list (filt=['hostname']):
	logger.l.debug("Entered get_node_list")
	ret = []

	allnodes = []

	for (plcapi,plprefix) in globals.plcaccess:
			s = xmlrpclib.ServerProxy(globals.plcapi, allow_none=True)
			auth = dict(AuthMethod='anonymous')

			if globals.nodegroup:
				logger.l.debug("Collecting nodes in nodegroup %s" % globals.nodegroup)
				ng = s.GetNodeGroups(auth, {'name' : globals.nodegroup})
				nodes = s.GetNodes(auth, ng[0]['node_ids'])

			elif globals.nodegroup_exclude:
				logger.l.debug("Collecting all nodes except in nodegroup %s" % globals.nodegroup_exclude)

				# Get nodegroup nodes
				ng = s.GetNodeGroups(auth, {'name' : globals.nodegroup_exclude})
				ng_nodes = s.GetNodes(auth, ng[0]['node_ids'])

				# Get all nodes
				all_nodes = s.GetNodes(auth, {'peer_id': None}, filt)
				
				# remove ngnodes from all node list
				ng_list = [ x['hostname'] for x in ng_nodes ]
				all_list = [ x['hostname'] for x in all_nodes ]
				not_ng_nodes = Set(all_list) - Set(ng_list)

				# keep each node that *is* in the not_ng_nodes set
				nodes = filter(lambda x : x['hostname'] in not_ng_nodes, all_nodes)

			else:
				logger.l.debug("Collecting all nodes")
				nodes = s.GetNodes(auth, {'peer_id': None}, filt)
				

			for node in nodes:
				try:
					ip = socket.gethostbyname(node['hostname'])
					if 'node_id' in filt:
						ret.append((ip,node['node_id']))
					else:
						ret.append(ip)
				except socket.gaierror:
					pass
			allnodes.append((plprefix,ret))
	return allnodes

if __name__ == "__main__":
	file_get_node_list (['hostname'], 'green')

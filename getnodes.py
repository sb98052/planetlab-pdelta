#!/usr/bin/python

import socket
import xmlrpclib
import globals
import logger
import os
import pdb

from sets import Set

def getListFromFile(file):
    f = open(file, 'r')
    list = []
    for line in f:
        line = line.strip()
        fields = line.split()
        list += [(fields[0],fields[1],0)]
    return list

def setFileFromList(list,file):
    f = open(file, 'w')
    for n in list:
        print >>f, "%s %s" % (n[0],n[1])
    f.close()

def file_get_node_list(filter=['hostname'], file='green'):
    allnodes = []

    try:
        allnodes = raw_get_node_list(filter)
        # Drop the prefix for create_silkconf
        nodes = [(n[1],n[2]) for n in allnodes]
        # Call this only once, because it overwrites the previous version of the conffile-->
        logger.l.debug("Creating '%s' file", file)
        setFileFromList(allnodes, file)
    except OSError:
        logger.log("%s: could not write to file." % file)
        logger.log("Should not continue without backup node list.")
        sys.exit(1)
    except:
        import traceback
        print traceback.print_exc()

        # api error, or other.
        # Read the node list
        if (os.path.exists(file)):
            try:
                allnodes = getListFromFile(file)
                # Drop the prefix for create_silkconf
                nodes = [(n[1],n[2]) for n in allnodes]
                # Create silkconf anyway        
            except OSError:
                logger.log("%s: file not found." % file)
                logger.log("Cannot continue without node list.")
                sys.exit(1)

    return allnodes

def raw_get_node_list (filt=['hostname']):
    logger.l.debug("Entered get_node_list")
    ret = []

    allnodes = []

    base_node_id=0
    for (plcapi,plprefix,auth) in globals.plcaccess:
            s = xmlrpclib.ServerProxy(plcapi, allow_none=True)

            if globals.nodegroup:
                logger.l.debug("Collecting nodes in nodegroup %s" % globals.nodegroup)
                ng = s.GetNodeGroups(auth, {'name' : globals.nodegroup})
                pdb.set_trace()
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
                    ret.append((plprefix,ip,base_node_id+node['node_id']))
                except socket.gaierror:
                    logger.l.debug("Socket error: could not look up %s"%node['hostname'])   
                    pass
            base_node_id=base_node_id+len(ret)
    return ret

if __name__ == "__main__":
    file_get_node_list (['hostname'], 'green')

#!/usr/bin/python
# pdelta - Collects Netflow data from all over planetlab and imports it into Silk

import optparse
import time
import os
import sys
import pdb
import bw

import logger
import nodeselector
import globals
import datasync

cur_bandwidth = 5

def bandwidth_used (s1,s2,i):
	mbdif = (s2-s1)>>20
	return mbdif/i

def main ():
		logger.l.info("Starting pdelta...")
		# Main loop. Get a fistful of nodes and sync them. Do this repeatedly.
		#pdb.set_trace ()
		nodeselector.reinit ()
		concurrency = 0
		pending_set = {}

		while True:
				global cur_bandwidth
				cur_node = nodeselector.get_next_pending ()
				if cur_node not in pending_set:
					data_sync_thread = datasync.DataSyncThread.new_thread (cur_node, pending_set)
				else:
					print "%s IS IN PROGRESS!!!"  % cur_node
					time.sleep (globals.wait_between_spawns) 
					# check that the node hasn't been taking too long.
					# possibly kill the thread and restart it...
					continue
				concurrency = concurrency + 1
				stamp1 = bw.get_cur_bytecount ()
				time.sleep (globals.wait_between_spawns) 
				stamp2 = bw.get_cur_bytecount ()
				if (bandwidth_used (stamp1,stamp2,globals.wait_between_spawns) >  globals.max_bandwidth and globals.do_bw_limit):
					# We're out of bandwidth. Wait for one of the sync threads to finish downloading
					logger.log("Concurrency = %d" % concurrency)
					datasync.DataSyncThread.done_download_event.wait ()




				







main ()

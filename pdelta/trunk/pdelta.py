#!/usr/bin/python
# pdelta - Collects Netflow data from all over planetlab and imports it into Silk

import optparse
import time
import os
import sys

import logger
import nodeselector
import globals
import datasync

def bandwidth_used ():
	return 5

def main ():
		# Main loop. Get a fistful of nodes and sync them. Do this repeatedly.
		while True:
				concurrency = 0
				while (bandwidth_used () <  globals.max_bandwidth):
						cur_node = nodeselector.get_next_pending ()
						data_sync_thread = datasync.DataSyncThread.new_thread (cur_node)
						concurrency = concurrency + 1
						time.sleep (globals.wait_between_spawns) 

				# We're out of bandwidth. Wait for one of the sync threads to finish downloading

				logger.log("Concurrency = %d" % concurrency)
				datasync.done_download_event.wait ()

	
		
		



				







main ()

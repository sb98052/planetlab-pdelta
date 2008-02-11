#!/usr/bin/python

import os
import threading
import globals
import logger

class DataSyncThread(threading.Thread):
	done_download_event = threading.Event() 

	def __init__(self,node):
		threading.Thread.__init__(self)
		self.ip = node

	def start_download (self):
			local_tmpdir = "%s/%s" % (globals.tmpdir,self.ip)
			rsync_command = "rsync -az %s@%s:%s/pf* %s"%(globals.slice_name,self.ip,globals.path,local_tmpdir)
			logger.log (rsync_command)

			if (not os.path.isdir(local_tmpdir)):
					mkdir(local_tmpdir)
			
			rp = os.popen (rsync_command)
			newfiles = rp.readlines ()
			# Will the previous line block? XXX
			return newfiles

	def start_import(self,newfiles):
			for f in newfiles:
					print "importing %s\n" % f

	def run(self):
			lst = self.start_download ()
			DataSyncThread.done_download_event.set()
			DataSyncThread.done_download_event.clear()
			self.start_import (lst)

		
	def new_thread(ip):
		sc = DataSyncThread(ip)
		sc.start()

	new_thread = staticmethod(new_thread)

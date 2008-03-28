#!/usr/bin/python

import os
import threading
import globals
import logger
import re
import random

import_exp = re.compile(r'(pf2.\d+)')

class DataSyncThread(threading.Thread):
	done_download_event = threading.Event() 

	def __init__(self,node, pending_set):
		threading.Thread.__init__(self)
		self.ip = node
		self.pending_set = pending_set
		pending_set[node] = True

	def start_download (self):
			local_tmpdir = "%s/%s" % (globals.tmpdir,self.ip)
			rsync_command = "rsync -avz %s@%s:%s/pf* %s"%(globals.slice_name,self.ip,globals.path,local_tmpdir)
			logger.l.info(rsync_command)

			if (not os.path.isdir(local_tmpdir)):
					os.mkdir(local_tmpdir)
			
			rp = os.popen (rsync_command)
			newfiles = rp.readlines ()
			return newfiles

	def start_import(self,newfiles):
			local_tmpdir = "%s/%s" % (globals.tmpdir,self.ip)
			files_done = []
			print "starting import for %s" % self.ip
			for f in newfiles:
				res = import_exp.search(f)
				if (res != None):
					fname = res.groups()[0]
					cmd = """rwflowpack --input-mode=file """ + \
						  """--netflow-file=%(globaltmp)s/%(ip)s/%(pffile)s """ + \
			  			  """--sensor-configuration=%(globaltmp)s/%(ip)s/sensor.conf """ + \
						  """--root-directory=%(silkdatadir)s """ + \
			  			  """--log-directory=%(globaltmp)s/%(ip)s/ """ + \
						  """--site-config-file=silk.conf""" 
					cmd = cmd % {'ip': self.ip, 'silkdatadir' : globals.silkdatadir, 
								 'globaltmp': globals.tmpdir, 'pffile': fname}
					print cmd
					os.system(cmd)
					files_done.append(fname)
			print "ending   import for %s %s" % (self.ip,files_done)

	def run(self):
			r = random.randint(1,10000)
			print "%s STARTING %s" % (self.ip, r)
			lst = self.start_download ()
			DataSyncThread.done_download_event.set()
			DataSyncThread.done_download_event.clear()
			self.start_import (lst)
			print "%s ENDING   %s" % (self.ip, r)
			del self.pending_set[self.ip]

		
	def new_thread(ip, pending_set):
		sc = DataSyncThread(ip, pending_set)
		sc.start()

	new_thread = staticmethod(new_thread)

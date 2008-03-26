#!/usr/bin/python

import os
import threading
import globals
import logger
import re

import_exp = re.compile(r'(pf2.\d+)')

class DataSyncThread(threading.Thread):
	done_download_event = threading.Event() 

	def __init__(self,node):
		threading.Thread.__init__(self)
		self.ip = node

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
			for f in newfiles:
				res = import_exp.search(f)
				if (res != None):
					fname = res.groups()[0]
					import_command = "silk_import %s %s/%s"%(self.ip,globals.tmpdir,fname)
					cmd = """rwflowpack --input-mode=file --netflow-file=%(globaltmp)s/%(pffile)s """ + \
			  			  """--sensor-configuration=%(globaltmp)s/data/%(ip)s/sensor.conf """ + \
						  """--root-directory=/data/ """ + \
			  			  """--log-directory=%(globaltmp)s/data/%(ip)s/ """ + \
						  """--site-config-file=out.conf""" 
					cmd = cmd % {'ip': self.ip, 'globaltmp': globals.tmpdir, 'pffile': fname}
					print import_command
					#os.system(cmd)

	def run(self):
			lst = self.start_download ()
			DataSyncThread.done_download_event.set()
			DataSyncThread.done_download_event.clear()
			self.start_import (lst)

		
	def new_thread(ip):
		sc = DataSyncThread(ip)
		sc.start()

	new_thread = staticmethod(new_thread)

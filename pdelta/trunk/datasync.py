#!/usr/bin/python

import os
import threading
import globals
import logger
import re
import random

import_exp = re.compile(r'(pf2.\d+)')
rsync_err = re.compile(r'link_stat ".*" failed: No such file or directory')
def rsync_error_in_output(newfiles, host):
	for f in newfiles:
		res = rsync_err.search(f)
		if (res != None):
			logger.l.info("found an error for %s on line : %s" % (host, f))
			return True
	
	return False

def files_todo(newfiles):
	files_todo = []
	for f in newfiles:
		res = import_exp.search(f)
		if (res != None):
			fname = res.groups()[0]
			files_todo.append(fname)
	return files_todo
	

class DataSyncThread(threading.Thread):
	done_download_event = threading.Event() 

	def __init__(self,node, pending_set):
		threading.Thread.__init__(self)
		self.ip = node
		self.pending_set = pending_set
		pending_set[node] = True

	def start_download (self):
		local_tmpdir = "%s/%s" % (globals.rawdatadir,self.ip)
		for remote_path in globals.paths:
			rsync_command = "rsync -avz %s@%s:%s/pf* %s"%(globals.slice_name,self.ip,
			                                              remote_path,local_tmpdir)
			logger.l.info(rsync_command)

			if (not os.path.isdir(local_tmpdir)):
				os.mkdir(local_tmpdir)
		
			(rp_in, rp_outerr) = os.popen4 (rsync_command)
			# read all output
			newfiles = rp_outerr.readlines ()
			# scan each line for pf2.* file
			files = files_todo(newfiles)
			# if there are errors or empty file, then search next path.
			if rsync_error_in_output(newfiles, self.ip) or files == []:
				continue
			else:
				return files

		logger.l.info("All globals.paths failed on host %s" % self.ip)
		return []

	#def start_download_old (self):
	#		local_tmpdir = "%s/%s" % (globals.rawdatadir,self.ip)
	#		rsync_command = "rsync -avz %s@%s:%s/pf* %s"%(globals.slice_name,self.ip,globals.path,local_tmpdir)
	#		logger.l.info(rsync_command)
	#
	#		if (not os.path.isdir(local_tmpdir)):
	#				os.mkdir(local_tmpdir)
	#		
	#		rp = os.popen (rsync_command)
	#		newfiles = rp.readlines ()
	#		return newfiles

	def start_import(self,newfiles):
			local_tmpdir = "%s/%s" % (globals.rawdatadir,self.ip)
			files_done = []
			print "starting import for %s" % self.ip
			for f in newfiles:
				res = import_exp.search(f)
				if (res != None):
					fname = res.groups()[0]
					cmd = """%(silkpath)s/sbin/rwflowpack --input-mode=file """ + \
						  """--netflow-file=%(rawdatadir)s/%(ip)s/%(pffile)s """ + \
			  			  """--sensor-configuration=%(rawdatadir)s/%(ip)s/sensor.conf """ + \
						  """--root-directory=%(silkdatadir)s """ + \
						  # Logging wastes a lot of space. 
						  # Let's disable it till we fix this in Silk - Sapan.
			  			  """--log-destination=none """ + \
			  			  #"""--log-directory=%(rawdatadir)s/%(ip)s/ """ + \
						  """--site-config-file=silk.conf""" 
					cmd = cmd % {'ip': self.ip, 
								 'silkdatadir' : globals.silkdatadir, 
								 'rawdatadir': globals.rawdatadir, 
								 'pffile': fname,
								 'silkpath' : globals.silkpath}
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

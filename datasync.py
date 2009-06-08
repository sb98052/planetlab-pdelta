#!/usr/bin/python

import os
import threading
import globals
import logger
import re
import random
import time
import pdb

import_exp = re.compile(r'(\d+)')
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

    def __init__(self,node, pending_set, prefix):
        threading.Thread.__init__(self)
        self.ip = node
        self.pending_set = pending_set
        self.slice_name = prefix + "_sapan"
        pending_set[node] = True

    def start_download (self):
        local_tmpdir = "%s/%s" % (globals.rawdatadir,self.ip)
        for remote_path in globals.paths:
            rsync_command = "rsync -r --timeout 30 -avzu %s@%s:%s %s"%(self.slice_name,self.ip,
                                                          remote_path,local_tmpdir)
            logger.l.info(rsync_command)

            if (not os.path.isdir(local_tmpdir)):
                os.mkdir(local_tmpdir)
        
            (rp_in, rp_outerr) = os.popen4 (rsync_command)
            # read all output
            newfiles = rp_outerr.readlines ()

            #pdb.set_trace()
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
    #       local_tmpdir = "%s/%s" % (globals.rawdatadir,self.ip)
    #       rsync_command = "rsync -avz %s@%s:%s/pf* %s"%(globals.slice_name,self.ip,globals.path,local_tmpdir)
    #       logger.l.info(rsync_command)
    #
    #       if (not os.path.isdir(local_tmpdir)):
    #               os.mkdir(local_tmpdir)
    #       
    #       rp = os.popen (rsync_command)
    #       newfiles = rp.readlines ()
    #       return newfiles

    def start_import(self,newfiles):
            local_tmpdir = "%s/%s" % (globals.rawdatadir,self.ip)
            files_done = []
            for f in newfiles:
                res = import_exp.search(f)
                if (res != None):
                    fname = res.groups()[0]
                    cmd = """%(silkpath)s/sbin/rwflowpack --input-mode=file """ + \
                          """--netflow-file=%(rawdatadir)s/%(ip)s/%(pffile)s """ + \
                          """--sensor-configuration=%(rawdatadir)s/%(ip)s/sensor.conf """ + \
                          """--root-directory=%(silkdatadir)s """ + \
                          """--log-destination=none """ + \
                          """--site-config-file=silk.conf""" 
                    cmd = cmd % {'ip': self.ip, 
                                 'silkdatadir' : globals.silkdatadir, 
                                 'rawdatadir': globals.rawdatadir, 
                                 'pffile': fname,
                                 'silkpath' : globals.silkpath}
                    
                    #pdb.set_trace ()
                    os.system(cmd)
                    files_done.append(fname)
            return files_done           
    
    def flat_to_heirarchical(self,newfiles):
            pdb.set_trace ()
            local_tmpdir = "%s/%s" % (globals.rawdatadir,self.ip)
            files_done = []
            for f in newfiles:
                ts = int(f)
                if (ts>1000000):
                    lo = ts%1000;
                    med = (ts/1000)%1000;
                    hi = (ts/1000000)%1000;

                    ts_path="%s/%s"%(local_tmpdir,f)
                    subdir_path="%03d/%03d/%03d"%(hi,med,lo)
                    dir_path="%s/%s"%(local_tmpdir,subdir_path)

                    cmd = "mkdir -p %s"%dir_path
                    print cmd
                    os.system(cmd)

                    cmd = "cp -lR %s/* %s"%(ts_path,dir_path)
                    print cmd
                    os.system(cmd)
                    cmd = "rm -fR %s"%(ts_path)
                    print cmd
                    os.system(cmd)
                    files_done.append(dir_path)
            return files_done           

    

    def fool_rsync(self, newfiles):
            local_tmpdir = "%s/%s" % (globals.rawdatadir,self.ip)       
            
            for f in newfiles:
                res = import_exp.search(f)
                if (res != None):
                    fname = res.groups()[0]
                    filename = "%s/%s" % (local_tmpdir, fname)
                    mtime=os.stat(filename).st_mtime
                    FILE = open(filename,"w")
                    FILE.truncate(0)
                    FILE.close()
                    # Change?? What change?
                    os.utime(filename, (mtime+60,mtime+60))

                    
            
    def time_stamp(self):
            local_tmpdir = "%s/%s" % (globals.rawdatadir,self.ip)
            ts_file = "%s/%s" % (local_tmpdir,"timestamp")
            FILE = open(ts_file,"w")
            FILE.write("%f" % time.time())
            FILE.close()
            
        
    def run(self):
            r = random.randint(1,10000)
            lst = self.start_download ()

            globals.concurrency = globals.concurrency - 1
            files_done = self.flat_to_heirarchical (lst)
            self.time_stamp ()
            
            print "Done with %s [%s]" % (self.ip,files_done)
            DataSyncThread.done_download_event.set()
            DataSyncThread.done_download_event.clear()
            globals.concurrency = globals.concurrency - 1
            del self.pending_set[self.ip]

        
    def new_thread(ip, pending_set,prefix):
        sc = DataSyncThread(ip, pending_set,prefix)
        sc.start()

    new_thread = staticmethod(new_thread)

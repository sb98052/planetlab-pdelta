
# Shamelessly stolen from the Node Manager

import os, sys
import subprocess
import time
import traceback
import logging as l

LOG_FILE = '/var/log/pdelta'

l.basicConfig(level=l.DEBUG,
                    format='%(asctime)s %(name)-8s : %(message)s',
                    filename=LOG_FILE,
                    filemode='aw')

def log(msg):
    """Write <msg> to the log file."""
    try:
        fd = os.open(LOG_FILE, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0600)
        if not msg.endswith('\n'): msg += '\n'
        os.write(fd, '%s: %s' % (time.asctime(time.gmtime()), msg))
        os.close(fd)
    except OSError:
        sys.stderr.write(msg)
        sys.stderr.flush()

def log_call(*args):
    log('running command %s' % ' '.join(args))
    try: subprocess.call(args, close_fds=True)
    except: log_exc()

def log_exc():
    """Log the traceback resulting from an exception."""
    log(traceback.format_exc())

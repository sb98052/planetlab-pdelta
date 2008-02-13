import globals
import re

dev_pattern = re.compile(r'eth0:(\d+)')

def get_cur_bytecount ():
	ret = -1
	try:
		f = open("/proc/net/dev");
		lines = f.readlines ()
		f.close ()
		
	except OSError:
		return ret
	
	for l in lines:
		global dev_pattern
		res = dev_pattern.search (l)
		if (res != None):
			bc = res.groups () [0]
			ret = int(bc)

	return ret

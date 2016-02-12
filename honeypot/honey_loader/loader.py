import os
import threading
import thread
import sys
import re

#sets path for reading in .py files to plugins folder
path = os.path.dirname(os.path.realpath(__file__)).replace("honey_loader", "plugins")
sys.path.insert(0, path)

path = path.replace("plugins","")

text_file = open(path+"plugins.txt", "r")
lines = re.split('\n| ',text_file.read()) #regex for new line and blanks


def start_plugins():
	try:
		lock = threading.Lock()
		for i in lines:
			if i != '' and i[:1] != '#':		#ignore blank lines and comments starting with #
				plugin = __import__(i)
				plugin.server_plugin(lock)

		while True:
			pass
	except KeyboardInterrupt:
		lock.acquire()
		print '\nexiting via KeyboardInterrupt'
		sys.exit()
		lock.release()
	except Exception as e:
		lock.acquire()
		print('ERROR: ' + str(e))
		sys.exit()
		lock.release()

if __name__ == '__main__':
	start_plugins()

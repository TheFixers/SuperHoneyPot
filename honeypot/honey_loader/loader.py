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


def start_plugin(class_to_run, socket_to_run):
    while 1:
        class_to_run(socket_to_run.accept()).start()

def start_plugins():
	for i in lines:
		if i != '' and i[:1] != '#':		#ignore blank lines and comments starting with #
			plugin = __import__(i)
			if i == "http_reader" or i == "http_reader2" or i == "ssh_plugin":   # currently the only two on the new format
				plugin.server_plugin()
			else:
				thread.start_new_thread(start_plugin, (plugin.Server, plugin.s,))

	while True:
		pass

if __name__ == '__main__':
	start_plugins()

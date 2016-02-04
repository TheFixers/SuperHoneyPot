import os
import threading
import thread
import sys

#sets path for reading in .py files to plugins folder
path = os.path.dirname(os.path.realpath(__file__))+os.path.sep+"plugins"
sys.path.insert(0, path)

text_file = open("plugins.txt", "r")
lines = text_file.read().split('\n')

def start_plugin(class_to_run, socket_to_run):
    while 1:
        class_to_run(socket_to_run.accept()).start()

for i in lines:
	plugin = __import__(i)
	if i == "http_reader" or i == "http_reader2":
		plugin.server_plugin()
	else:
		thread.start_new_thread(start_plugin, (plugin.Server, plugin.s,))

while True:
	pass

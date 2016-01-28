from src import telnet_reader
# from src import http_reader
from src import https_reader
from src import ssh_plugin
import thread


def start_telnet(class_to_run, socket_to_run):
    while 1:
        class_to_run(socket_to_run.accept()).start()


try:
    thread.start_new_thread(start_telnet, (telnet_reader.Server, telnet_reader.s,))
    thread.start_new_thread(start_telnet, (https_reader.Server, https_reader.s,))
    thread.start_new_thread(start_telnet, (ssh_plugin.Server, ssh_plugin.s,))
    # thread.start_new_thread(start_telnet, (http_reader.Server, http_reader.s,))

except:
    print "Error: unable to start thread"

while 1:
    pass

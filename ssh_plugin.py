__author__ = 'daemoniclegend'

import socket, threading, time

host = ''
sshport = 22


srvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srvr.bind((host, sshport))
srvr.listen(5)
lock = threading.Lock()

class ssh_plugin(threading.Thread):

    track_data = []

    def __init__(self, (socket, address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address

    def run(self):
        print 'Connection with %s:%s' % self.address
        self.time = time.ctime(time.time())
        self.socket.send('Login as: ')

        self.track_data = [self.time, self.address, self.socket, sshport]



while True:
    ssh_plugin(srvr.accept()).start()


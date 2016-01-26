#__author__ = 'daemoniclegend'

import time
import socket
import threading

HOST = ''
PORT = 22


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
lock = threading.Lock()


class Server(threading.Thread):

    track_data = []

    def __init__(self, (socket, address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.time = time

    def run(self):
        print 'Connection with %s:%s' % self.address
        self.time = time.ctime(time.time())
        self.socket.send('Login as: ')

        self.track_data = [self.time, self.address, self.socket, sshport]




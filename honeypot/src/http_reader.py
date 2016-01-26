#
# Got this from:
# http://stackoverflow.com/questions/6487772/simple-telnet-chat-server-in-python
#

import threading
import socket

HOST = ''
PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)

clients = []
lock = threading.Lock()


class Server(threading.Thread):
    def __init__(self, (socket,address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address

    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        print '%s:%s connected HTTP.' % self.address
        # while True:
        #     data = self.socket.recv(1024)
        #     if not data:
        #         break
        #     for c in clients:
        #         c.socket.send(data)
        self.socket.close()
        print '%s:%s disconnected HTTP.' % self.address
        lock.acquire()
        clients.remove(self)
        lock.release()

"""
    This file is part of SuperHoneyPot.

    SuperHoneyPot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SuperHoneyPot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with SuperHoneyPot.  If not, see <http://www.gnu.org/licenses/>.
"""

'''
    Simple socket server using threads
'''
import threading
import socket
import sys
import signal
from thread import *

HOST = ''
PORT = 23


class server_plugin(threading.Thread):
    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.daemon = True
        self.start()

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket to local host and port
        try:
            s.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        # Start listening on socket
        s.listen(4)
        self.lock.acquire()
        print 'Started telnet server on port ', PORT
        self.lock.release()

        # now keep talking with the client
        while 1:
            # wait to accept a connection - blocking call
            conn, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(clientthread, (conn, addr))

        s.close()


# Function for handling connections. This will be used to create threads
def clientthread(conn, addr):
    line = ''
    i = 0
    conn.send('\n')
    conn.send('\n')
    conn.send('Login authentication\n')
    conn.send('\n')
    conn.send('\n')
    conn.send('Username: ')
    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from client
        data = conn.recv(1024)

        if "\n" in data:
            data = data.replace('\r\n', '')
            if i == 0:
                print 'Username attempted: ' + data
                conn.send('Password: ')
                i = i + 1
            elif i == 1:
                print 'Password attempted: ' + data
                i = i + 1
            elif data == 'quit' or data == 'q' or data == 'QUIT' or data == 'Q':
                print addr[0] + ':' + str(addr[1]) + ': ' + 'Connection terminated.'
                break
            else:
                print addr[0] + ':' + str(addr[1]) + ': ' + data  # repr()
        if not data:
            print addr[0] + ':' + str(addr[1]) + ': ' + 'Connection terminated.'
            break

    conn.close()


if __name__ == '__main__':
    try:
        lock = threading.Lock()
        server_plugin(lock)
        while True:
            pass
    except KeyboardInterrupt:
        print '\nexiting via KeyboardInterrupt'

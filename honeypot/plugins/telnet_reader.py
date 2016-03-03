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
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()

    def run(self):

        #Bind socket to local host and port
        try:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        
        #Start listening on socket
        self.s.listen(4)
        self.lock.acquire()
        print 'Started telnet server on port ', PORT
        self.lock.release()

        #now keep talking with the client
        while 1:
            #wait to accept a connection - blocking call
            conn, addr = self.s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            client_thread(self.lock, conn, addr)

        try:
            while True:
                pass
        except KeyboardInterrupt, IOError:
                self.tear_down()

    def tear_down(self):
        print 'closing'        
        self.s.close()

#Class for handling connections. This will be used to create threads
class client_thread(threading.Thread):


    def __init__(self, lock, conn, addr):
        threading.Thread.__init__(self)
        self.lock = lock
        self.conn = conn
        self.addr = addr
        self.daemon = True
        self.start()

    def run(self):
        global datarecieved
        line = ''
        i = 0
        self.conn.send('\n')
        self.conn.send('\n')
        self.conn.send('Login authentication\n')
        self.conn.send('\n')
        self.conn.send('\n')
        self.conn.send('Username: ')
        #infinite loop so that function do not terminate and thread do not end.
        datarecieved = ''
        linux = True

        while True:

            #Receiving from client
            data = self.conn.recv(1024)
            # print repr(data)
            if "\r\n" in data or '\r\x00' in data:
                datarecieved = datarecieved + data
                datarecieved = datarecieved.replace('\r\n','')
                datarecieved = datarecieved.replace('\r\x00','')
                # print repr(datarecieved)
                if i == 0:
                    print 'Username attempted: ' + datarecieved
                    self.conn.send('password: ')
                    i = i + 1
                elif i == 1:
                    print 'Password attempted: ' + datarecieved
                    if linux:
                        self.conn.send('>> ')
                    i = i + 1
                else:
                    print self.addr[0] + ':' + str(self.addr[1]) + ': ' + datarecieved # repr() 
                    if '\r\x00' in data:
                        self.conn.send('\n?Invalid command\n')
                    else:
                        self.conn.send('?Invalid command\n')
                    if linux:
                        self.conn.send('>> ')
                datarecieved = ""
            # first line on connection with linux is this giant string so just removing that nonsense
            elif not '\xff\xfd\x03\xff\xfb\x18\xff\xfb\x1f\xff\xfb \xff\xfb!\xff\xfb"\xff\xfb\'\xff\xfd\x05\xff\xfb#' == data : 
                if 0 == i:
                    linux = False
                datarecieved = datarecieved + data

            # these two are ctrl+c in linux and in windows. Easier way to end program. 
            if '\xff\xf4\xff\xfd\x06' == data or '\x03' == data or not data:
                print self.addr[0] + ':' + str(self.addr[1]) + ': ' +'Connection terminated.'
                break

        self.conn.close()


if __name__ == '__main__':
    try:
        lock = threading.Lock()
        server_plugin(lock)
        while True:
            pass
    except KeyboardInterrupt:
        print '\nexiting via KeyboardInterrupt'
        sys.exit()


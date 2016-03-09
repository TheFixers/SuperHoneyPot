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
import datetime
import time
import threading
import socket
import sys
import signal
import json
import os


path = os.path.dirname(os.path.realpath(__file__)).replace("plugins", "db_interface")
sys.path.insert(0, path)

import honeypot_db_interface

 
HOST = '' 
PORT = 23
ERROR = 'error from Telnet plugin: '

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
            self.lock.acquire()
            print ERROR + 'Bind failed. ' + str(msg[0]) + ' Message ' + msg[1]
            self.lock.release()
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
            self.lock.acquire()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            self.lock.release()
            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            client_thread(self.lock, conn, addr)

        try:
            while True:
                pass
        except KeyboardInterrupt, IOError:
                self.tear_down()

    def tear_down(self):
        self.lock.acquire()
        print 'telnet closing'   
        self.lock.release()     
        self.s.close()

#Class for handling connections. This will be used to create threads
class client_thread(threading.Thread):

    interface = honeypot_db_interface.honeypot_database_interface()

    def __init__(self, lock, conn, addr):
        threading.Thread.__init__(self)
        self.lock = lock
        self.conn = conn
        self.ip = addr[0]    # explination of (ip, port) in addr 
        self.socket = addr[1]  # http://stackoverflow.com/questions/12454675/whats-the-return-value-of-socket-accept-in-python
        self.username = ''
        self.password = ''
        self.time = datetime.datetime.now().time()
        self.data = ''
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
                    if len(datarecieved) > 128:
                        self.username = datarecieved[0:127]
                    else:
                        self.username = datarecieved
                    if not linux:
                        self.conn.send('                    ')
                    self.conn.send('password: ')
                    i = i + 1
                elif i == 1:
                    if len(datarecieved) > 128:
                        self.password = datarecieved[0:127]
                    else:
                        self.password = datarecieved
                    if linux:
                        self.conn.send('>> ')
                    else:
                        self.conn.send('               ')
                    i = i + 1
                else:
                    if self.data == '':
                        self.data = datarecieved
                    else:
                        self.data = self.data +" || "+ datarecieved
                    if '\r\x00' in data:
                        self.conn.send('\nInvalid command\n')
                    else:
                        self.conn.send('Invalid command\n')
                    if linux:
                        self.conn.send('>> ')
                    i = i+1
                datarecieved = ""
            # first line on connection with linux is this giant string so just removing that nonsense
            elif not '\xff\xfd\x03\xff\xfb\x18\xff\xfb\x1f\xff\xfb \xff\xfb!\xff\xfb"\xff\xfb\'\xff\xfd\x05\xff\xfb#' == data : 
                if 0 == i:
                    linux = False
                datarecieved = datarecieved + data

            # these two are ctrl+c in linux and in windows. Easier way to end program. 
            if i == 7 or '\xff\xf4\xff\xfd\x06' == data or '\x03' == data or not data:
                self.lock.acquire()
                print self.ip + ':' + str(self.socket) + ': ' +'Connection terminated.'
                self.lock.release()
                break

            if len(self.data) > 128 :
                self.data = self.data[0:127]
                break

        self.conn.close()
        self.send_output()

    def send_output(self):
        # creates an output string to be sent to the database (via interface)
        dump_string = json.dumps({'Client':{'IP':self.ip,'Port':PORT.__str__(), 'Socket':str(self.socket),
                                            'Data':{'Time':self.time.__str__(),
                                                    'Username':self.username,
                                                    'Passwords':self.password,
                                                    'Data':self.data}}})

        self.lock.acquire()
        print('Telnet Attack: ' + self.time.__str__() + ' from ' + self.ip + ' on port ' + PORT.__str__() + '.')
        client_thread.interface.receive_data(dump_string)        
        self.lock.release()
        return


if __name__ == '__main__':
    try:
        lock = threading.Lock()
        server_plugin(lock)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print '\nexiting via KeyboardInterrupt'
        sys.exit()



#!/usr/bin/python2

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

import time
import threading
import socket
import sys
import json
import os


path = os.path.dirname(os.path.realpath(__file__)).replace("plugins", "db_interface")
sys.path.insert(0, path)

import honeypot_db_interface

 
HOST = ''
ERROR = 'Error Source:: Telnet Plugin. '

class server_plugin(threading.Thread):

    def __init__(self, lock, port):
        threading.Thread.__init__(self)
        self.port = int(float(port))
        self.lock = lock
        self.daemon = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()

    def run(self):

        #Bind socket to local host and port
        try:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((HOST, self.port))
        except socket.error as msg:
            self.lock.acquire()
            print ERROR + 'Error Number: ' + str(msg[0])
            print '    Port: ' + str(self.port) + ', Message: ' + msg[1]
            self.lock.release()
            sys.exit()

        
        #Start listening on socket
        self.s.listen(4)
        self.lock.acquire()
        print 'Started telnet server on port ', self.port
        self.lock.release()

        #now keep talking with the client
        while 1:
            #wait to accept a connection - blocking call
            conn, addr = self.s.accept()  
            self.lock.acquire()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            self.lock.release()
            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            client_thread(self.lock, conn, addr, self.port)

        try:
            while True:
                pass
        except KeyboardInterrupt, IOError:
                self.tear_down()

    def tear_down(self):
        print 'telnet '+str(self.port)+' closing'  
        
        try:
            self.s.close()
        except AttributeError:
            self.lock.acquire()
            print ERROR + 'AttributeError.'

#Class for handling connections. This will be used to create threads
class client_thread(threading.Thread):

    interface = honeypot_db_interface.honeypot_database_interface()

    def __init__(self, lock, conn, addr, port):
        threading.Thread.__init__(self)
        self.port = port
        self.lock = lock
        self.conn = conn
        self.ip = addr[0]    # explination of (ip, port) in addr 
        self.socket = addr[1]  # http://stackoverflow.com/questions/12454675/whats-the-return-value-of-socket-accept-in-python
        self.username = ''
        self.password = ''
        self.time = time.time()
        self.data = ''
        self.daemon = True
        self.start()

    def run(self):
        global datarecieved

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
        overFlow = False

        while True:

            #Receiving from client
            data = self.conn.recv(4096)
            # print repr(data)
            if len(data) == 4096:
                if overFlow:
                    if self.data == '':
                        self.data = 'OVERFLOW ATTEMPT'
                    else:
                        self.data = ' || OVERFLOW ATTEMPT'
                    break
                overFlow = True;

            if '\xff\xf3\xff\xfd\x06' in data :
                data.replace('\xff\xf3\xff\xfd\x06',' ctrl+\\')
            elif "\r\n" in data or '\r\x00' in data :

                datarecieved = datarecieved + data
                datarecieved = datarecieved.replace('\r\n','')
                datarecieved = datarecieved.replace('\r\x00','')
                datarecieved = datarecieved.replace('\xff\xf3\xff\xfd\x06',' ctrl+\\')

                if i == 0:
                    if len(datarecieved) > 128:
                        self.username = datarecieved[0:127]
                    else:
                        self.username = datarecieved
                    if not linux:
                        self.conn.send('                    ')
                    self.conn.send('password: ')
                    i += 1
                elif i == 1:
                    if len(datarecieved) > 128:
                        self.password = datarecieved[0:127]
                    else:
                        self.password = datarecieved
                    if linux:
                        self.conn.send('>> ')
                    else:
                        self.conn.send('               ')
                    i += 1
                else:
                    overFlow = False
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
                    i += 1
                datarecieved = ""
            # first line on connection with linux is this giant string so just removing that nonsense
            elif not '\xff\xfd\x03\xff\xfb\x18\xff\xfb\x1f\xff\xfb \xff\xfb!\xff\xfb"\xff\xfb\'\xff\xfd\x05\xff\xfb#' == data : 
                if 0 == i:
                    linux = False
                datarecieved = datarecieved + data

            # these two are ctrl+c in linux and in windows. Easier way to end program. 
            if i == 12 or '\xff\xf4\xff\xfd\x06' == data or '\x03' == data or not data:
                self.lock.acquire()
                print self.ip + ':' + str(self.socket) + ': ' + 'Connection terminated.'
                self.lock.release()
                break

            if len(self.data) > 128 :
                self.data = self.data[0:127]
                break

        self.conn.close()
        self.send_output()

    def send_output(self):
        # creates an output string to be sent to the database (via interface)
        dump_string = json.dumps({'Client':{'TYPE':"Telnet",'IP':self.ip,'Port':self.port.__str__(), 'Socket':str(self.socket),
                                            'Data':{'Time':self.time.__str__(),
                                                    'Username':self.username,
                                                    'Passwords':self.password,
                                                    'Data':self.data}}})

        self.lock.acquire()
        print('Telnet Attack: ' + self.time.__str__() + ' from ' + self.ip + ' on port ' + self.port.__str__() + '.')
        client_thread.interface.receive_data(dump_string)        
        self.lock.release()
        return


if __name__ == '__main__':
    try:
        lock = threading.Lock()
        server_plugin(lock, 23)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print '\nexiting via KeyboardInterrupt'
        sys.exit()



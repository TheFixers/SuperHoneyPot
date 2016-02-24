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

        #Bind socket to local host and port
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

        #Start listening on socket
        s.listen(4)
        self.lock.acquire()
        print 'Started telnet server on port ', PORT
        self.lock.release()

        #now keep talking with the client
        while 1:
            #wait to accept a connection - blocking call
            conn, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            client_class(self.lock, conn, addr)
         
        s.close()

#Class for handling connections. This will be used to create threads
class client_class(threading.Thread):


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
            print repr(data)
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
            elif not '\xff\xfd\x03\xff\xfb\x18\xff\xfb\x1f\xff\xfb \xff\xfb!\xff\xfb"\xff\xfb\'\xff\xfd\x05\xff\xfb#' == data :
                if 0 == i:
                    linux = False
                datarecieved = datarecieved + data
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


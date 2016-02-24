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
            start_new_thread(clientthread ,(conn, addr))
         
        s.close()

#Function for handling connections. This will be used to create threads
def clientthread(conn, addr):
    global datarecieved
    line = ''
    i = -1
    conn.send('\n')
    conn.send('\n')
    conn.send('Login authentication\n')
    conn.send('\n')
    conn.send('\n')
    conn.send('Username: ')
    #infinite loop so that function do not terminate and thread do not end.

    while True:
        
        if i == -1:
            datarecieved = ''
            print 'here'
            linux = True
            i = 0

        #Receiving from client
        data = conn.recv(1024)

        if '\r\n' in data:
            datarecieved = datarecieved + data

        if "\r\n" in datarecieved:
            datarecieved = datarecieved.replace('\r\n','')
            # print repr(datarecieved)
            if i == 0:
                print 'Username attempted: ' + datarecieved
                conn.send('password: ')
                i = i + 1
            elif i == 1:
                print 'Password attempted: ' + datarecieved
                if linux:
                    conn.send('>> ')
                i = i + 1
            elif datarecieved == 'quit' or datarecieved == 'q' or datarecieved == 'QUIT' or datarecieved == 'Q' or datarecieved == 'exit':
                print addr[0] + ':' + str(addr[1]) + ': ' +'Connection terminated.'
                break
            else:
                print addr[0] + ':' + str(addr[1]) + ': ' + datarecieved # repr() 
                if linux:
                    conn.send('>> ')
            datarecieved = ""
        elif len(data) == 1:
            linux = False
            datarecieved = datarecieved + data
            print 'here again'
        if not data:
            print addr[0] + ':' + str(addr[1]) + ': ' +'Connection terminated.'
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
        sys.exit()


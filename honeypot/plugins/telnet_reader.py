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
    line = ''
    i = 0
    conn.send('\n')
    conn.send('\n')
    conn.send('Login authentication\n')
    conn.send('\n')
    conn.send('\n')
    conn.send('Username: ')
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        

        #Receiving from client
        data = conn.recv(1024)
        
        if "\n" in data:
            if i == 0:
                print 'Username attempted: ' + line[9:]
                conn.send('                Password: ')
            if i == 1:
                print 'Password attempted: ' + line[9:]
            if line == 'quit' or line == 'q' or line == 'QUIT' or line == 'Q':
                print addr[0] + ':' + str(addr[1]) + ': ' +'Connection terminated.'
                conn.close()
                break
            print addr[0] + ':' + str(addr[1]) + ': ' + line
            i = i + 1
            line = ''
        else: line = line + data
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


'''
    Simple socket server using threads
'''
import threading
import socket
import sys
from thread import *
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 23 # Arbitrary non-privileged port

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
            start_new_thread(clientthread ,(conn,))
         
        s.close()

 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    line = ''
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        if "\n" in data:
            print line
            line = ''
        line = line + data
        if not data: 
            break
     
    #came out of loop
    conn.close()


if __name__ == '__main__':
        lock = threading.Lock()
        server_plugin(lock)
        while True:
            pass


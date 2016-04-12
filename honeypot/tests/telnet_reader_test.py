#!/usr/bin/python2

import os
import sys
import unittest
import socket
import threading
import thread
import time

# would be used for integration tests
path = os.path.dirname(os.path.realpath(__file__)).replace("tests", "plugins")
sys.path.insert(0, path)
import telnet_reader

path = os.path.dirname(os.path.realpath(__file__)).replace("tests","plugins")
sys.path.insert(0,path)
path = path.replace("plugins","")
#import plugin
'''
GeneralServerTest
TestCase1: test_run: Checks to see if the plugin with start and up
TestCase2: test_teardown: Checks to see if the plugin will close ports and shut down correctly
TestCase3: test_invalidport: Checks to see if the server is only listen on the assigned port
TestCase4: test_mulithreads: Checks to see if the server can accept multiple connections at once


'''

PORT = 23

class telent_client(threading.Thread):
    def run(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(("localhost", PORT))
        self.conn.recv(1024)




class GeneralTelnetReaderTest(unittest.TestCase):
   # Checks to see if the server will start and accept a valid connection
    def test_startUp(self):
        try:
            lock = threading.Lock()
            self.telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:

            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(("localhost", PORT))
            #

            self.conn.recv(1024)

            connection = True
            self.telnet.s.close()
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)

            time.sleep(1)

    def test_run(self):
        time.sleep(1)
        try:
            lock = threading.Lock()
            self.telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")


        time.sleep(1)
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(("localhost", PORT))

            for x in range(0, 1):
                self.conn.recv(1024)
            self.conn.sendall('Username \r\n')
            msg = self.conn.recv(1024)
            print msg
            self.conn.send('Password \r\n')
            msg = self.conn.recv(1024)
            print msg
            self.conn.send('Command test \r\n')
            msg = self.conn.recv(1024)
            print msg
            self.conn.send('\x03')
            msg = self.conn.recv(1024)
            print msg
            self.telnet.s.close()
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)

            self.conn.close()
            time.sleep(1)


    # Checks to see if the server will shutdown properly
    def test_teardown(self):
        connection = False
        try:
              lock = threading.Lock()
              self.telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
              self.fail("Server Failed to Start")

        time.sleep(1)

        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(("localhost", PORT))
            self.conn.recv(1024)
            self.conn.sendall('Username \r\n')
            self.conn.recv(1024)
            self.conn.send('Password \r\n')
            self.conn.recv(1024)
            self.conn.send('Command test \r\n')
            self.conn.recv(1024)
            self.conn.send('\x03')
            self.conn.recv(1024)

            connection = True
        except Exception as e:
            print e
            self.fail("client failed to connect")

        try:
            self.telnet.tear_down()
            self.conn.connect(("localhost",PORT))
            self.telnet.s.close()
            self.fail("Server Failed to shutdown")
        except Exception as e:
            self.assertTrue(True)
        finally:
            self.conn.close()
            time.sleep(1)

    def test_invalidport(self):
        try:
            lock = threading.Lock()
            telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", PORT-1))
            connection = True
        except Exception as e:
            connection = False
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", PORT+1))
            connection = True
        except Exception as e:
            connection = False
        finally:
            self.assertFalse(connection)
            conn.close()
    #test if the client tries to overflow the buffer
    def test_bufferoverflow(self):
        buff = '\x41'* 16793598
        bufferOverflow = False
        time.sleep(1)
        try:
            lock = threading.Lock()
            self.telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(("localhost", PORT))
            self.conn.settimeout(30.0)
            msg = self.conn.recv(1024)
            # print msg
            self.conn.sendall('Username \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('Password \r\n')
            msg = self.conn.recv(1024)
            # print msg
            start = time.time()
            self.conn.sendall('' + buff + buff + ' \r\n')
            self.conn.sendall('\r\n')
            msg = self.conn.recv(1024)
            if msg != 'Invalid command\n>> ':
                bufferOverflow = True
            else:
                bufferOverflow = False
            self.conn.send('\x03')
            self.conn.recv(1024)
            self.conn.settimeout(30.0)
            self.telnet.s.close()
            connection = True
        except Exception as e:
            if e.message == 'timed out':
                self.fail('Client had to timeout: 30 seconds')
            print e
            connection = False
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(("localhost", PORT))
            self.conn.recv(1024)
            self.conn.sendall('Username \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('Password \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('Command test \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('\x03')
            msg = self.conn.recv(1024)
            # print msg
            self.telnet.s.close()
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection & bufferOverflow)
            self.conn.close()
            time.sleep(1)


    ##test if the client tries to overflow the buffer
    def test_bufferoverflow(self):
        buff = '\x41'* 16793598
        bufferOverflow = False
        time.sleep(1)
        try:
            lock = threading.Lock()
            self.telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(("localhost", PORT))
            self.conn.settimeout(5.0)
            msg = self.conn.recv(1024)
            # print msg
            self.conn.sendall('Username \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('Password \r\n')
            msg = self.conn.recv(1024)
            # print msg
            start = time.time()
            self.conn.sendall('' + buff + buff + ' \r\n')
            self.conn.sendall('\r\n')
            msg = self.conn.recv(1024)
            if msg != 'Invalid command\n>> ':
                bufferOverflow = True
            else:
                bufferOverflow = False
            self.conn.send('\x03')
            self.conn.recv(1024)
            self.conn.settimeout(30.0)
            self.telnet.s.close()
            connection = True
        except Exception as e:
            if e.message == 'timed out':
                self.fail('Client had to timeout: 30 seconds')
            print e
            connection = False
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect(("localhost", PORT))
            self.conn.recv(1024)
            self.conn.sendall('Username \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('Password \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('Command test \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('\x03')
            msg = self.conn.recv(1024)
            # print msg
            self.telnet.s.close()
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection & bufferOverflow)
            self.conn.close()
            time.sleep(1)


    #Test to make sure that server is listening on multiple threads
    #Ignore error that it has to many threads running.
    # def test_mulithreads(self):
    #     try:
    #          lock = threading.Lock()
    #          telnet = telnet_reader.server_plugin(lock, PORT)
    #     except Exception as e:
    #         self.fail("Server Failed to Start")
    #     time.sleep(1)
    #     try:
    #         threads = []
    #         for num in range(0, 4):
    #             thread = telent_client()
    #             thread.start()
    #             threads.append(thread)
    #         telnet.s.close()
    #         for thread in threads:
    #             thread.join()
    #
    #         connection = True
    #     except Exception as e:
    #         print e
    #         connection = False
    #     finally:
    #         self.assertTrue(connection)
    #         # telnet.server.close()
    #         time.sleep(1)


'''
This will test some of more commmon ways to break in

TestCase1: test_sql_injection:
TestCase2: test_buffer_overflow:
TestCase3: test_null:
'''


'''
class CommonBreakInAttempts(unittest.TestCase):
    def test_sql_injection(self):
        self.assertTrue(False)
    def test_buffer_overflow(self):
        self.assertTrue(False)
    def test_null(self):
        self.assertTrue(False)
'''


if __name__ == '__main__':
    unittest.main()
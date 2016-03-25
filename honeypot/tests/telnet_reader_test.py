#!/usr/bin/python2

import os
import sys
import unittest
import socket
import threading
import thread

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
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(("localhost", 23))

class GeneralTelnetReaderTest(unittest.TestCase):

    # Checks to see if the server will start and accept a valid connection
    def test_startUp(self):
        try:
            lock = threading.Lock()
            telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", 23))
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)
            conn.close()

    def test_run(self):

        try:
            lock = threading.Lock()
            telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")



        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", 23))

            conn.recv(1024)
            conn.recv(1024)
            conn.recv(1024)
            conn.recv(1024)
            conn.recv(1024)
            conn.recv(1024)
            conn.sendall('Username \r\n')
            conn.recv(1024)
            conn.send('Password \r\n')
            conn.recv(1024)
            conn.send('Command test \r\n')
            conn.send('\x03')

            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)
            conn.close()


    # Checks to see if the server will shutdown properly
    def test_teardown(self):
         connection = False
         try:
             lock = threading.Lock()
             telnet = telnet_reader.server_plugin(lock, PORT)
         except Exception as e:
             print e
             self.fail("server failed to start")

         try:
             conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             conn.connect(("localhost", 23))

             conn.recv(1024)
             conn.recv(1024)
             conn.recv(1024)
             conn.recv(1024)
             conn.recv(1024)
             conn.recv(1024)
             conn.send('Username \r\n')
             conn.recv(1024)
             conn.send('Password \r\n')
             conn.recv(1024)
             conn.send('Command test \r\n')
             conn.send('\x03')
         except Exception as e:
             print e
             self.fail("Client failed to make a connection")

         try:
             telnet.tear_down()
             conn.connect(("localhost",23))
         except Exception as e:
             self.assertTrue(True)
         finally:
             self.fail("Server Failed to shutdown")
             conn.close()

    def test_invalidport(self):
        try:
            lock = threading.Lock()
            telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", 22))
            connection = True
        except Exception as e:
            connection = False
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", 24))
            connection = True
        except Exception as e:
            connection = False
        finally:
            self.assertFalse(connection)
            conn.close()
    #
    #Test to make sure that server is listening on multiple threads
    #Ignore error that it has to many threads running.
    def test_mulithreads(self):
        try:
             lock = threading.Lock()
             telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")

        try:
            threads = []
            for num in range(0, 4):
                thread = telent_client()
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)


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
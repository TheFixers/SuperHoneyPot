#!/usr/bin/python2
# -*- coding:  UTF-8 -*-

import os
import sys
import unittest
import socket
import threading
import thread
import time

path = os.path.dirname(os.path.realpath(__file__)).replace("tests", "plugins")
sys.path.insert(0, path)
import telnet_reader
path = os.path.dirname(os.path.realpath(__file__)).replace("tests","plugins")
sys.path.insert(0,path)
path = path.replace("plugins","")
'''

TestCase0: test_startUp: Checks to see if the server will start and accept a valid connection
TestCase1: test_run: Checks to see if the plugin with start and up
TestCase2: test_teardown: Checks to see if the plugin will close ports and shut down correctly
TestCase3: test_invalidport: Checks to see if the server is only listen on the assigned port
TestCase4: test_mulithreads: Checks to see if the server can accept multiple connections at once
TestCase5: test_nonacsii: see if the sever can handle nonascii character and ctl+[char]
TestCase6: test_shellshock: shell shock test
TestCase7: test_bufferoverflow: test if the client tries to overflow the buffer

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
            self.conn.recv(1024)
            connection = True

            self.telnet.s.close()
            self.conn.close()
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)

            time.sleep(1)
    # Checks to see if the telnet plugin with start and communicate with a single client
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
    # test invalidports make sure the plus or minus one port is not activated by this plugin
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
            telnet.s.close()
            conn.close()

    #Test to make sure that server is listening on multiple threads
    def test_mulithreads(self):
        try:
             lock = threading.Lock()
             telnet = telnet_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:
            threads = []
            for num in range(0, 4):
                thread = telent_client()
                thread.start()
                threads.append(thread)
            telnet.s.close()
            for thread in threads:
                thread.join()

            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            telnet.s.close()
            self.assertTrue(connection)
            # telnet.server.close()
            time.sleep(1)

    # see if the sever can handle nonascii character and ctl+[char]
    def test_nonacsii(self):
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
            self.conn.recv(1024)
            self.conn.sendall('Username \r\n')
            self.conn.recv(1024)
            self.conn.send('Password \r\n')
            self.conn.recv(1024)
            self.conn.send('café \r\n')
            self.conn.recv(1024)
            self.conn.send('ñóǹ äŝçíì 汉语/漢語  华语/華語 Huáyǔ; 中文 Zhōngwén 漢字仮名交じり文 Lech Wałęsa æøå \r\n')
            self.conn.recv(1024)
            self.conn.send(
                '\x00 \x01 \x02 \x04 \x05 \x06 \x07 \x08 \x09 \x0A \x0B \x0C \x0D \x0E \x0F'
                '\x20 \x21 \x22 \x23 \x24 \x25 \x26 \x27 \x28 \x29 \x2A \x2B \x2C \x2D \x2E \x2F'
                '  \r\n')
            self.conn.recv(1024)
            '''

            self.conn.sendall(
                '\x10' '\x13'' \x11 ' '\x12' '\x14 ' '\x15 ' '\x16 ' '\x17 ' '\x18 ' '\x19 ' '\x1A '
                '\x1B ' '\x1C ' '\x1D ' '\x1E ' '\x1F'
                '\r\n')

            self.conn.recv(1024)
            '''
            self.conn.send('\x03')
            self.conn.recv(1024)
            self.telnet.s.close()
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)
            self.conn.close()
            time.sleep(1)

    # shell shock test
    def test_shellshock(self):
        shellshockfail = False
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
            msg = self.conn.recv(1024)
            # print msg
            self.conn.sendall('Username \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('Password \r\n')
            msg = self.conn.recv(1024)
            # print msg
            self.conn.send('env z="() { :; }; echo vulnerable" bash -c "echo foo"'' \r\n')
            msg = self.conn.recv(1024)
            # print msg
            if msg in 'vulnerable':
                shellshockfail = False
                self.fail("ShellShock occured: " + msg)
            else:
                shellshockfail = True
            self.conn.send('\x03')
            self.conn.recv(1024)
            self.telnet.s.close()
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection & shellshockfail)
            self.conn.close()
            time.sleep(1)

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


if __name__ == '__main__':
    unittest.main()
#!/usr/bin/python2
# -*- coding:  UTF-8 -*-

import os
import sys
import unittest
import threading
import socket
import paramiko
import time
'''
# would be used for integration tests
path = os.path.dirname(os.path.realpath(__file__)).replace("tests", "honey_loader")
sys.path.insert(0, path)
path = path.replace("honey_loader","")
import loader
'''

path = os.path.dirname(os.path.realpath(__file__)).replace("tests","plugins")
sys.path.insert(0,path)
path = path.replace("plugins","")
import ssh_plugin
'''
GeneralServerTest
TestCase1: test_run: Checks to see if the plugin with start and up
TestCase2: test_teardown: Checks to see if the plugin will close ports and shut down correctly
TestCase3: test_invalidport: Checks to see if the server is only listen on the assigned port
TestCase4: test_mulithreads: Checks to see if the server can accept multiple connections at once


'''
PORT  = 22

class SSHClient():
    def start(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(("localhost", PORT))

    def run(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect('localhost', PORT, username='local@localhost', password='True')
    def close(self):
        self.ssh.close
    def stop(self):
        self.conn.close
class GeneralServerTest(unittest.TestCase):

    # Checks to see if the server will start and accept a valid connection
    def test_startUp(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", PORT))
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)
            conn.close()
            sshServer.s.close()
            time.sleep(1)

    # Checks to see if the server will start and accept a valid connection
    # The SSH Server is designed to have authentication failed no matter what username and password is enter
    def test_run(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('localhost', PORT, username='local@localhost', password='True')
            connection = True
        except Exception as e:
            #Currently SSH is design to fail on any password.
            if e.message == 'Authentication failed.':
                connection = True
            else:
                print e
                connection = False
        finally:
            self.assertTrue(connection)
            ssh.close()
            time.sleep(1)



    # Checks to see if the server will shutdown properly
    def test_teardown(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:
            sshServer.tear_down()
            ssh = paramiko.SSHClient()
            # ssh.load_host_keys('dummypublickey')
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('localhost', PORT, username='local@localhost', password='True')
            connection = False
        except Exception as e:
        # Currently SSH is design to fail on any password.
            if e.message == "'server_plugin' object has no attribute 'teardown'":
                print e.message
                connection = False
            else:
                # print e.message
                connection = True
        finally:
            self.assertTrue(connection)



# makes sure the server doesn't accept invalid port
#     def test_invalidPort(self):
#         try:
#             lock = threading.Lock()
#             sshServer = ssh_plugin.server_plugin(lock, PORT)
#         except Exception as e:
#             self.fail("Server Failed to Start")
#         try:
#             ssh = paramiko.SSHClient()
#             ssh.load_host_keys('dummypublickey')
#             # ssh.load_system_host_keys()
#             ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#             ssh.connect('localhost', 21, username='local@localhost', password='True')
#             # ssh.connect('localhost', 22)
#             connection = False
#         except Exception as e:
#             #Currently SSH is design to fail on any password.
#             if e.message == 'Authentication failed.':
#                 connection = False
#             else:
#                 print e
#                 connection = True
#         try:
#             ssh = paramiko.SSHClient()
#             ssh.load_host_keys('dummypublickey')
#             # ssh.load_system_host_keys()
#             ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#             ssh.connect('localhost', 23, username='local@localhost', password='True')
#             # ssh.connect('localhost', 22)
#             connection = False
#         except Exception as e:
#             #Currently SSH is design to fail on any password.
#             if e.message == 'Authentication failed.':
#                 connection = False
#             else:
#                 print e
#                 connection = True
#         finally:
#             self.assertTrue(connection)
#             ssh.close()


    # not sure how to make this occur yet
    # Makes sure the server can accept multiple request at once
    def test_multithreads(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:
            threads = []
            for num in range(0, 4):
                thread = SSHClient()
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.stop()
            connection = True
        except paramiko.AuthenticationException:
                connection = False
        except Exception as e:
            connection = False
        finally:
            self.assertTrue(connection)
            time.sleep(1)

    def test_nonacsii(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock, PORT)
        except Exception as e:
            print("Server Failed to Start")
        time.sleep(1)
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            ssh.connect('localhost', username='ñóǹ äŝçíì 汉语/漢語  华语/華語 Huáyǔ; 中文 Zhōngwén 漢字仮名交じり文 Lech Wałęsa æøå',
                        password='/x03')

            connection = True
        except Exception as e:
            if e.message == 'Authentication failed.':
                connection = True
            else:
                print e
                connection = False
        finally:
            print(connection)
            ssh.close()
            time.sleep(1)

    def test_buffoverflower(self):

        buff = '\x41'* 16793598

        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock, PORT)
        except Exception as e:
            print("Server Failed to Start")
        time.sleep(1)
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            ssh.connect('localhost', username='' + buff,
                        password=''+buff+buff)

            connection = True

        except Exception as e:
            if e.message == 'Authentication failed.':
                connection = True
            else:
                print e
                connection = False
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            ssh.connect('localhost', username='user',
                        password='pass')

        except Exception as e:
            if e.message == 'Authentication failed.':
                connection = True
            else:
                print e
                connection = False

        finally:
            print(connection)
            ssh.close()
            time.sleep(1)







    def shell_shock_test (self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock, PORT)
        except Exception as e:
            print("Server Failed to Start")
        time.sleep(1)
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
            ssh.connect('localhost', username='root@localhost',
                        password='env z="() { :; }; echo vulnerable" bash -c "echo foo"')

            connection = True
        except Exception as e:
            if e.message == 'Authentication failed.':
                connection = True
            else:
                print e
                connection = False
        finally:
            print(connection)
            ssh.close()
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
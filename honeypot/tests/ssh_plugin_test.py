#!/usr/bin/python2

import os
import sys
import unittest
import threading
import socket
import paramiko

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

class GeneralServerTest(unittest.TestCase):

    # Checks to see if the server will start and accept a valid connection
    def test_startUp(self):
        try:
            lock = threading.Lock()
            telnet = ssh_plugin.server_plugin(lock)
        except Exception as e:
            self.fail("Server Failed to Start")

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(("localhost", 22))
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)
            conn.close()

    # Checks to see if the server will start and accept a valid connection
    def test_run(self):

        try:
            lock = threading.Lock()
            telnet = ssh_plugin.server_plugin(lock)
        except Exception as e:
            self.fail("Server Failed to Start")

        try:
            ssh = paramiko.SSHClient()
            ssh.load_host_keys('dummypublickey')
            # ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('localhost', 22, username='UnitTest', password='True')
            # ssh.connect('localhost', 22)
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)
            ssh.close()




    # Checks to see if the server will shutdown properly
    def test_teardown(self):
        self.assertTrue(False)

    # makes sure the server doesn't accept invalid port
    def test_invalidPort(self):
        self.assertTrue(False)

    # Makes sure the server can accept multiple request at once
    def test_multithreads(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
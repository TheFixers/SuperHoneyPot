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

import os
import sys
import unittest
import threading
import socket
import paramiko
import time


path = os.path.dirname(os.path.realpath(__file__)).replace("tests","plugins")
sys.path.insert(0,path)
path = path.replace("plugins","")
import ssh_plugin
'''
The SSH Server is designed to have authentication failed no matter what username and password is enter

TestCase0: test_startUp: Checks to see if the plugin will start up
TestCase1: test_run: Checks to see if the plugin will start up and run
TestCase2: test_teardown: Checks to see if the plugin will close ports and shut down correctly
TestCase3: test_invalidport: Checks to see if the server is only listen on the assigned port
TestCase4: test_mulithreads: Checks to see if the server can accept multiple connections at once
TestCase5: test_nonacsii: see if the sever can handle nonascii character and ctl+[char]
TestCase6: test_shellshock: shell shock test
TestCase7: test_bufferoverflow: test if the client tries to overflow the buffer

'''
PORT = 22


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

            if e.message == 'Authentication failed.':
                connection = True

            else:
                print e
                connection = False

        finally:
            self.assertTrue(connection)
            ssh.close()
            time.sleep(1)

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
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('localhost', PORT, username='local@localhost', password='True')
            connection = False
            sshServer.s.close()

        except Exception as e:
        # Currently SSH is design to fail on any password.
            if e.message == "'server_plugin' object has no attribute 'teardown'":
                print e.message
                connection = False

            else:
                connection = True

        finally:
            self.assertTrue(connection)

    '''
    def test_invalidPort(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        try:
            ssh = paramiko.SSHClient()
            ssh.load_host_keys('dummypublickey')
            # ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('localhost', 21, username='local@localhost', password='True')
            # ssh.connect('localhost', 22)
            connection = False
        except Exception as e:
            #Currently SSH is design to fail on any password.
            if e.message == 'Authentication failed.':
                connection = False
            else:
                print e
                connection = True
        try:
            ssh = paramiko.SSHClient()
            ssh.load_host_keys('dummypublickey')
            # ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('localhost', 23, username='local@localhost', password='True')
            # ssh.connect('localhost', 22)
            connection = False
        except Exception as e:
            #Currently SSH is design to fail on any password.
            if e.message == 'Authentication failed.':
                connection = False
            else:
                print e
                connection = True
        finally:
            self.assertTrue(connection)
            ssh.close()
    '''

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

    def test_shellshock (self):
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

    def test_bufferoverflow(self):
        buff = '\x41' * 16793598 # sends 16,793,598 A
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
            ssh.connect('localhost', username='' + buff + buff,
                        password='' + buff + buff)
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
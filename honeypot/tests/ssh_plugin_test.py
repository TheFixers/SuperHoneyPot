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
class SSHClient():
    def start(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_host_keys('dummypublickey')
        # ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect('localhost', 22, username='local@localhost', password='True')
    def close(self):
        self.ssh.close

class GeneralServerTest(unittest.TestCase):

    # Checks to see if the server will start and accept a valid connection
    def test_startUp(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock)
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
    # The SSH Server is designed to have authentication failed no matter what username and password is enter
    def test_run(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock)
        except Exception as e:
            self.fail("Server Failed to Start")

        try:
            ssh = paramiko.SSHClient()
            ssh.load_host_keys('dummypublickey')
            # ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('localhost', 22, username='local@localhost', password='True')
            # ssh.connect('localhost', 22)
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




    # Checks to see if the server will shutdown properly
    def test_teardown(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock)
        except Exception as e:
            self.fail("Server Failed to Start")
        try:
            sshServer.teardown()
            ssh = paramiko.SSHClient()
            ssh.load_host_keys('dummypublickey')
            # ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('localhost', 22, username='local@localhost', password='True')
            # ssh.connect('localhost', 22)
            connection = False
        except Exception as e:
        # Currently SSH is design to fail on any password.
            if e.message == 'Authentication failed.':
                connection = False
            else:
                print e.message
                connection = True
        finally:
            self.assertTrue(connection)


# makes sure the server doesn't accept invalid port
    def test_invalidPort(self):
        try:
            lock = threading.Lock()
            sshServer = ssh_plugin.server_plugin(lock)
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


    # not sure how to make this occur yet
    # Makes sure the server can accept multiple request at once
    # def test_multithreads(self):
    #     try:
    #         lock = threading.Lock()
    #         sshServer = ssh_plugin.server_plugin(lock)
    #     except Exception as e:
    #         self.fail("Server Failed to Start")
    #     try:
    #         threads = []
    #         for num in range(0, 4):
    #             thread = SSHClient()
    #             thread.start()
    #             threads.append(thread)
    #
    #         for thread in threads:
    #             thread.join()
    #         connection = True
    #     except paramiko.AuthenticationException:
    #             connection = True
    #     except Exception as e:
    #         connection = False
    #     finally:
    #         self.assertTrue(connection)


'''
shell shock test env z="() { :; }; echo vulnerable" bash -c "echo foo"
'''
if __name__ == '__main__':
    unittest.main()
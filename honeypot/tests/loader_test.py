import threading
import socket
import unittest
import os, imp
imp.load_source("loader", os.path.join(os.path.dirname(__file__), "..\honey_loader\loader.py"))
import loader
import dummy_plugin #not sure what this running on
import dummy_client
'''
    Since import dummy_plugin runs the plugin. You need to run


'''


class TestLoader(unittest.TestCase):

    # Test the method start_plugin(class_to_run, socket_to_run): with good inputs
    # Excepted that no errors occurs and a valid connection is made.
    def test_startplugin(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            threading._start_new_thread(loader.start_plugin,(dummy_plugin.server, dummy_plugin.sock))

            HOST = 'localhost'    # The remote host
            PORT = 23              # The same port as used by the server

            s.connect((HOST, PORT))

        except Exception as e:
            self.fail("The connection was not made")
        finally:
            s.close()

    # Test the method start_plugin(class_to_run, socket_to_run): with an default socket input
    # Excepted no error to occur and connection will be made
    def test_startplugin_invalidsocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 80)
            sock.bind(server_address)
            sock.listen(1)
            threading._start_new_thread(loader.start_plugin,(dummy_plugin.server, sock))

            HOST = 'localhost'    # The remote host
            PORT = 80              # The same port as used by the server

            s.connect((HOST, PORT))
        except Exception as e:
            self.fail("A connection was not made")
        finally:
            s.close()

    # Test the method start_plugin(class_to_run, socket_to_run): with a null inputs
    # Excepted AttributeError since socket_to_run does not have .accept()
    def test_startplugin_nullsocket(self):

        self.assertRaises(AttributeError, loader.start_plugin, (dummy_plugin.server, None))


    # Test the method start_plugin(class_to_run, socket_to_run): with a null inputs
    # Excepted AttributeError since class_to_run does not have .start()
    def test_startplugin_nullclass_to_run(self):
        self.assertRaises(AttributeError, loader.start_plugin,(None, dummy_plugin.sock))

    # Test the method start_plugin(class_to_run, socket_to_run): with an plugin invalid input
    def test_startplugin_invalidplugin(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:

            threading._start_new_thread(loader.start_plugin,(dummy_client.server, dummy_plugin.sock))

            HOST = 'localhost'    # The remote host
            PORT = 80              # The same port as used by the server

            s.connect((HOST, PORT))
            self.fail("Invalid class_to_run created a psuedo connection valid connection")
        except Exception as e:
            pass
        finally:
            s.close()



    def test_startplugins2(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
import dummy_plugin
import threading
import socket
import unittest
import os, imp
imp.load_source("loader", os.path.join(os.path.dirname(__file__), "..\honey_loader\loader.py"))
import loader

class TestLoader(unittest.TestCase):

    # Test the method start_plugin(class_to_run, socket_to_run): with good inputs
    def test_startplugin(self):
        threading._start_new_thread(loader.start_plugin,(dummy_plugin.Server, dummy_plugin.s))

        try:
            HOST = 'localhost'    # The remote host
            PORT = 23              # The same port as used by the server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
        except Exception as e:
            self.fail("The connection was not made")
        finally:
            s.close()
        self.assertTrue(False)

    #This will check the start plugin is really setting the ports or not.
    #def test_startpluginincorrectport(self):
     #   loader.start_plugin(dummy_plugin.Server,  24)
      #  try:
       #     HOST = ''    # The remote host
        #    PORT = 23              # The same port as used by the server
         #   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          #  s.connect((HOST, HOST))
       # except Exception as e:
        #    self.fail("The connection was not made")
        #finally:
         #   s.close()
         #   self.assertTrue(True)


    def test_startplugins2(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
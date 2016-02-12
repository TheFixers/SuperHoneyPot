import httplib
import os
import re
import sys
import unittest

path = os.path.dirname(os.path.realpath(__file__)).replace("tests", "honey_loader")
sys.path.insert(0, path)
path = path.replace("honey_loader","")
import loader

'''
   This will run test on the loader.

   Testcase1: test_start_plugins: Test is to see if good inputs will run and not throw any errors.
   Testcase2: test_start_plugins_IOError:  IOError is execpt to be thrown if plugin in file name is changed or is
   missing
   Testcase3: test_start_plugins_baddatainfile: There is Bad data in the file.
   Testcase4: test_start_plugins_blankfile: Blank file for input.
   Testcase5:
'''
path = os.path.dirname(os.path.realpath(__file__)).replace("honey_loader", "plugins")
sys.path.insert(0, path)
path = path.replace("plugins","")

class TestLoader(unittest.TestCase):

    # First test is to see if good inputs will run and not throw any errors.
    # expect no Exception to pass
    def test_start_plugins(self):
        dummy_file = open("dummy_plugins.txt", "w")
        dummy_file.write("http_reader\nhttp_reader2\ntelnet_reader\nhttps_reader\nssh_plugin\n")
        dummy_file.close()
        try:
            text_file = open("dummy_plugins.txt", "r")
            loader.lines = re.split('\n| ',text_file.read()) #regex for new line and blanks

            loader.start_plugins
            plugins = True
            '''
            # This will check that the plugin did load and start up a valid connection with the each plugin
            # http_reader2
            try:
                conn = httplib.HTTPSConnection("localhost", 80)
                http1 = True
                plugins = True
            except Exception as e:
                http1 = False
                 plugins = False
            finally:
                conn.close()
            # http_reader2
            try:
                conn = httplib.HTTPSConnection("localhost", 81)
                http2 = True
                 plugins = True
            except Exception as e:
                http2 = False
                 plugins = False
            finally:
                conn.close()
            # telnet_reader
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect(("localhost", 8888))
                telnet = True
                 plugins = True
            except Exception as e:
                telnet = False
                 plugins = False
            finally:
                conn.close()
            # https_reader
              try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect(("localhost", 8888))
                https = True
                 plugins = True
            except Exception as e:
                https = False
                 plugins = False
            # ssh_plugin
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect(("localhost", 22))
                ssh = True
                 plugins = True
            except Exception as e:
                ssh = False
                 plugins = False
            finally:
                conn.close()
            '''
        except Exception as e:
            # print e
            self.fail("Error has accorded")

        if not plugins:
            self.fail("One or more plugins are not being started by the loader")

    # IOError is execpt to be thrown if plugin in file name is changed or is missing.
    # except IOError to pass
    def test_start_plugins_IOError(self):
        os.remove("dummy_plugins.txt")
        try:
            text_file = open("dummy_plugins.txt", "r")
            loader.lines = re.split('\n| ',text_file.read()) #regex for new line and blanks

            loader.start_plugins
            self.fail("An IOError was execpted to be thrown")
        except IOError as e:
            self.assertTrue(True)

    # This will test what happens if there is a bad data in the file.
    # If bad data is in the file except that all plugins will still run or any plugin that is started to be
    # shutdown.
    def test_start_plugins_baddatainfile(self):
        dummy_file = open("dummy_plugins.txt", "w")
        dummy_file.write("http_reader\nhttp_reader2\ntelnet_reader\nhttps_reader\nbad\nssh_plugin\n")
        dummy_file.close()
        try:
            text_file = open("dummy_plugins.txt", "r")
            loader.lines = re.split('\n| ',text_file.read()) #regex for new line and blanks

            loader.start_plugins

            #self.fail("runs an invalid plugin")
        except AssertionError as e:
            pass
        finally:
            try:
                conn = httplib.HTTPSConnection("localhost", 80)
                plugins = True
            except Exception as e:
                plugins = False
            finally:
                conn.close()

        if(plugins):
            self.fail("some of the plugins are running while the loader")
        else:
            self.assertTrue(True)

    # This test if a blank file is used for inputs
    # Might choose to use warning on empty file
    def test_start_plugins_blankfile(self):
        dummy_file = open("dummy_plugins.txt", "w")
        # dummy_file.seek(99999) Optional test is to create a larger file with no data
        # dummy_file.write("\0")
        dummy_file.close()
        try:
            text_file = open("dummy_plugins.txt", "r")
            loader.lines = re.split('\n| ',text_file.read()) #regex for new line and blanks

            loader.start_plugins

        except Exception as e:
            self.fail("Error has accorded: " + e)


if __name__ == '__main__':
    unittest.main()
    os.remove("dummy_plugins.txt")
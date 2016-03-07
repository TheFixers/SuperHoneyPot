import httplib
import os
import re
import sys
import unittest

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
#import plugin
'''
GeneralServerTest
TestCase1: test_run: Checks to see if the plugin with start and up
TestCase2: test_teardown: Checks to see if the plugin will close ports and shut down correctly
TestCase3: test_invalidport: Checks to see if the server is only listen on the assigned port
TestCase4: test_mulithreads: Checks to see if the server can accept multiple connections at once


'''

class GeneralServerTest(unittest.TestCase):

    # Checks to see if the server will start and accept a valid connection
    def test_run(self):
        self.assertTrue(False)

    # Checks to see if the server will shutdown properly
    def test_teardown(self):
        self.assertTrue(False)

    # makes sure the server doesn't accept invalid port
    def test_invalidPort(self):
        self.assertTrue(False)

    # Makes sure the server can accept multiple request at once
    def test_multithreads(self):
        self.assertTrue(False)
'''
This tests will test the feature of the plugin

TestCase1: test_communication:

'''
class PluginSpeficTest(unittest.TestCase):
    def test_communication(self):
        self.assertTrue(False)
'''
This will test some of more commmon ways to break in

TestCase1: test_sql_injection:
TestCase2: test_buffer_overflow:
TestCase3: test_null:
'''
class CommonBreakInAttempts(unittest.TestCase):
    def test_sql_injection(self):
        self.assertTrue(False)
    def test_buffer_overflow(self):
        self.assertTrue(False)
    def test_null(self):
        self.assertTrue(False)



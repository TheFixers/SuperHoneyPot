import unittest
import sys
from ..src import ssh_plugin
sp = ssh_plugin



class GeneralServerTest(unittest.TestCase):
    # Checks to see if the server can start up.
    def test_init(self):
        self.assertTrue(False)

    # Checks to see if the server will accept a valid connection
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
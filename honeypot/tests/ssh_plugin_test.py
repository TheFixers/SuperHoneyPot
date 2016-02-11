<<<<<<< HEAD
import unittest
import sys
from ..plugins import ssh_plugin
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
=======
__author__ = 'daemoniclegend'

import os
import sys

path = os.path.dirname(os.path.realpath(__file__)).replace("tests", "plugins")
sys.path.insert(0, path)

from plugins import ssh_plugin
'''
path = os.getcwd().replace('UnitTest', '')
sys.path.insert(0, path)
sys.path.append('..')
'''

ssh_plugin.server_plugin()
>>>>>>> refs/remotes/origin/master

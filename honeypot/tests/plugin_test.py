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
TestCase5: Test_pluginSpeficTest:
TestCase6: test_sql_injection:
TestCase7: test_buffer_overflow:
TestCase8: test_null:

'''

class GeneralServerTest(unittest.TestCase):

    @unittest.expectedFailure
    def test_run(self):
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_teardown(self):
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_invalidPort(self):
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_multithreads(self):
        self.assertTrue(False)

class PluginSpeficTest(unittest.TestCase):
    @unittest.expectedFailure
    def test_communication(self):
        self.assertTrue(False)

class CommonBreakInAttempts(unittest.TestCase):
    @unittest.expectedFailure
    def test_sql_injection(self):
        self.assertTrue(False)
    @unittest.expectedFailure
    def test_buffer_overflow(self):
        self.assertTrue(False)
    @unittest.expectedFailure
    def test_null(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
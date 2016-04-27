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

import httplib
import os
import re
import sys
import unittest

path = os.path.dirname(os.path.realpath(__file__)).replace("tests", "honey_loader")
sys.path.insert(0, path)
import loader

'''

   Testcase0: test_start_plugins: Test is to see if good inputs will run and not throw any errors.
   Testcase1: test_start_plugins_IOError:  IOError is execpt to be thrown if plugin in file name is changed or is
   missing
   Testcase3: test_start_plugins_baddatainfile: There is Bad data in the file.
   Testcase4: test_start_plugins_blankfile: Blank file for input.
   Testcase5:
'''
path = path.replace("honey_loader", "plugins")
sys.path.insert(0, path)

path = path.replace("plugins","tests")

dummy_plugins_path = path + os.path.sep + 'dummy_plugins.txt'


class TestLoader(unittest.TestCase):

    def test_start_plugins(self):
        self.dummy_file = open(dummy_plugins_path, "w")
        self.dummy_file.write("http_reader\ntelnet_reader\nhttps_reader\nssh_plugin\n")
        self.dummy_file.close()

        try:
            text_file = open(dummy_plugins_path, "r")
            loader.lines = re.split('\n| ',text_file.read()) #regex for new line and blanks
            loader.start_plugins
            plugins = True

        except Exception as e:
            # print e
            self.fail("Error has accorded")

        if not plugins:
            self.fail("One or more plugins are not being started by the loader")

    def test_start_plugins_IOError(self):
        os.remove(dummy_plugins_path)
        try:
            text_file = open(dummy_plugins_path, "r")
            loader.lines = re.split('\n| ',text_file.read()) #regex for new line and blanks
            loader.start_plugins
            self.fail("An IOError was execpted to be thrown")

        except IOError as e:
            self.assertTrue(True)

    def test_start_plugins_baddatainfile(self):
        self.dummy_file = open(dummy_plugins_path, "w")
        self.dummy_file.write("http_reader\ntelnet_reader\nhttps_reader\nbad\nssh_plugin\n")
        self.dummy_file.close()
        start_plugins_exited = False
        try:
            text_file = open(dummy_plugins_path, "r")
            loader.lines = re.split('\n| ',text_file.read()) #regex for new line and blanks
            self.fail("runs an invalid plugin")

        except AssertionError as e:
            pass

        finally:

            if start_plugins_exited:
                plugins = True

                try:
                    conn = httplib.HTTPConnection('localhost', 80)

                except Exception as e:
                    plugins = False

                finally:
                    conn.close()

                if plugins:
                    self.fail("some of the plugins are running while the loader")

                else:
                    self.assertTrue(True)

    def test_start_plugins_blankfile(self):
        self.dummy_file = open(dummy_plugins_path, "w")
        # dummy_file.seek(99999) Optional test is to create a larger file with no data
        # dummy_file.write("\0")
        self.dummy_file.close()
        try:
            text_file = open(dummy_plugins_path, "r")
            loader.lines = re.split('\n| ',text_file.read()) #regex for new line and blanks
            loader.start_plugins
            text_file.close()

        except Exception as e:
            self.fail("Error has accorded: " + e)

        finally:
            self.dummy_file.close()
            os.remove(dummy_plugins_path)

if __name__ == '__main__':
    unittest.main()
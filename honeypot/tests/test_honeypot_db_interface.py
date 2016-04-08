import os
import sys
import unittest
import socket
import threading
import thread
import time

path = os.path.dirname(os.path.realpath(__file__)).replace("tests", "db_interface")
sys.path.insert(0, path)
import honeypot_db_inteface


class MongoDBIntefaceTest(unittest.TestCase):

    def test_bad_db_input(self):
        self.fail()

    def test_good_db_input(self):
        self.fail()

    def test_receive_data(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()


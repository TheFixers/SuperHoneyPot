import unittest
from ...honeypot import honeypot

hp = honeypot


class HoneyPotTest(unittest.TestCase):

    def test_start_telnet(self):
        self.assertTrue(False)
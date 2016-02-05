import unittest
from ..src import telnet_reader

tn = telnet_reader.Server


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


class TelnetUnitTest(unittest.TestCase):
    # The Port should be defaulted to 23;
    def test_default_port(self):
        self.assertEqual(tn.PORT, 23)

    # The default host right now is blank
    def test_default_host(self):
        self.assertEqual(tn.HOST, '')

    #
    def test_recv_username(self):
        self.assertTrue(False)

    def test_recv_password(self):
        self.assertTrue(False)

    def test_recv_invalid_response(self):
        self.assertTrue(False)

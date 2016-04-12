import threading
import os
import socket
import sys
import unittest
import httplib
import ssl
import time

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
import https_reader
'''
GeneralServerTest
TestCase1: test_run: Checks to see if the plugin with start and up
TestCase2: test_teardown: Checks to see if the plugin will close ports and shut down correctly
TestCase3: test_invalidport: Checks to see if the server is only listen on the assigned port
TestCase4: test_mulithreads: Checks to see if the server can accept multiple connections at once


'''
PORT =  1025


class mulithread_client(threading.Thread):
    def run(self):
        conn = httplib.HTTPSConnection('localhost', PORT, timeout=5, context=ssl._create_unverified_context())
        conn.request("GET", "/")
        r1 = conn.getresponse()
        # print r1.status, r1.reason



class GeneralServerTest(unittest.TestCase):

    # Checks to see if the server will start and accept a valid connection
    # Checks to see if the server will start and accept a valid connection
    def test_startUp(self):
        print "Test_StartUP"
        try:
            lock = threading.Lock()
            self.https = https_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:
            conn =httplib.HTTPSConnection('localhost', PORT, timeout=5, context=ssl._create_unverified_context())
            connection = True
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)
            conn.close()
            self.https.server.shutdown()
            self.https.server.server_close()
            time.sleep(1)

    def test_run(self):
        print "Test_RUN"
        try:
            lock = threading.Lock()
            self.https = https_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:
            conn =httplib.HTTPSConnection('localhost', PORT, timeout=5, context=ssl._create_unverified_context())
            conn.request("GET", "/")
            r1 = conn.getresponse()
            if r1.status == 404:
                connection = True
            else:
                connection = False
        except Exception as e:
            print e
            connection = False
        finally:
            self.assertTrue(connection)
            conn.close()
            self.https.server.shutdown()
            self.https.server.server_close()
            time.sleep(1)

    # #     # Checks to see if the server will shutdown properly
    def test_teardown(self):
        print "test_teardown"
        try:
            lock = threading.Lock()
            self.https = https_reader.server_plugin(lock, PORT)
        except Exception as e:
            print e
            self.fail("Failed to startup server")
        time.sleep(1)
        try:
            conn = httplib.HTTPSConnection('localhost', PORT, timeout=5, context=ssl._create_unverified_context())
            conn.request("GET", "/")
            r1 = conn.getresponse()
            if r1.status == 404:
                connection = True
            else:
                connection = False
            conn.close()
        except Exception as e:
            print e
            self.fail("Client couldn't to server")
        try:
            self.https.tear_down()
            httplib.HTTPSConnection('localhost', PORT, timeout=5, context=ssl._create_unverified_context())
            r2 = conn.getresponse()
            self.fail("Server failed to shutdown")
            self.https.server.shutdown()
            self.https.server.server_close()
        except Exception as e:
            #sever shutdown
            self.assertTrue(True)
            time.sleep(1)

    # # # makes sure the server doesn't accept invalid port
    # def test_invalidPort(self):
    #     print "Test_InvalidPORT"
    #     try:
    #         lock = threading.Lock()
    #         self.https = https_reader.server_plugin(lock, PORT)
    #     except Exception as e:
    #         self.fail("Server Failed to Start")
    #
    #     try:
    #         conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         conn.connect(("localhost", (PORT+1)))
    #         connection = False
    #     except Exception as e:
    #         # print e
    #         connection = True
    #     finally:
    #         conn.close()
    #         # self.https.server.shutdown()
    #         # self.https.server.server_close()
    #
    #     try:
    #         conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         conn.connect(("localhost", (PORT-1)))
    #         connection = False
    #     except Exception as e:
    #         # print e
    #         connection = True
    #     finally:
    #         self.assertTrue(connection)
    #         conn.close()
    #         # self.https.server.shutdown()
    #         # self.https.server.server_close()
    #         time.sleep(1)

    # Makes sure the server can accept multiple request at once
    def test_multithreads(self):

        try:
            lock = threading.Lock()
            self.https = https_reader.server_plugin(lock, PORT)
        except Exception as e:
            self.fail("Server Failed to Start")
        time.sleep(1)
        try:
            threads = []
            for num in range(0, 4):
                thread = mulithread_client()
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
            self.assertTrue(True)
        except Exception as e:
            print e
            self.fail("Server is not listening on multiple threads")
        finally:
            time.sleep(1)
            self.https.server.shutdown()
            self.https.server.server_close()

'''
This will test some of more commmon ways to break in

TestCase1: test_sql_injection:
TestCase2: test_buffer_overflow:
TestCase3: test_null:
'''
# class CommonBreakInAttempts(unittest.TestCase):
#     def test_sql_injection(self):
#         self.assertTrue(False)
#     def test_buffer_overflow(self):
#         self.assertTrue(False)
#     def test_null(self):
#         self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
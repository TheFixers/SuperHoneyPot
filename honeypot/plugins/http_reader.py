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

import socket
import json
import time
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import sys


path = os.path.dirname(os.path.realpath(__file__)).replace("plugins", "db_interface")
sys.path.insert(0, path)

import honeypot_db_interface

ERROR = 'Error Source:: HTTP Plugin. '

class server_plugin(threading.Thread):

    interface = honeypot_db_interface.honeypot_database_interface()

    def __init__(self, lock, port):
        threading.Thread.__init__(self)
        self.port = int(float(port))
        self.lock = lock
        self.daemon = True
        self.start()

    def run(self):

        # Create a web server and define the handler to manage the
        # incoming request

        try:
            self.server = HTTPServer(('', self.port), web_server_handler)
            self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.lock.acquire()
            print 'Started http server on port ', self.port
            self.lock.release()
            # Wait forever for incoming htto requests
            self.server.serve_forever()

        except KeyboardInterrupt, IOError:
            self.tear_down()

        except socket.error as msg:
            self.lock.acquire()
            print ERROR + 'Error Number: ' + str(msg[0])
            print '    Port: ' + str(self.port) + ', Message: ' + msg[1]
            self.lock.release()
            sys.exit()


    def tear_down(self):
        print 'HTTP '+str(self.port)+' closing'
        # self.server.socket.close()
        self.server.shutdown()
        self.server.server_close()


class web_server_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_error(404, 'File Not Found: %s' % self.path)

        client_url = self.path
        client_ip = self.client_address  # ip and port
        request_time = time.time()

        json_data = {'Client': {'TYPE':"HTTP",'IP': client_ip[0],'Port':str(self.server.server_address[1]),'Socket':str(client_ip[1]),
                                'Data':{'Time':request_time.__str__(),'clientURL':client_url}}}
        # export to db or something here
        data = json.dumps(json_data)
        print('HTTP Attack: ' + request_time.__str__() + ' on port ' + str(self.server.server_address[1]) + '.')
        server_plugin.interface.receive_data(data)


        # try:
        #     #Check the file extension required and
        #     #set the right mime type
        #
        #     sendReply = False
        #     if self.path.endswith(".html"):
        #         mimetype='text/html'
        #         sendReply = True
        #     if self.path.endswith(".jpg"):
        #         mimetype='image/jpg'
        #         sendReply = True
        #     if self.path.endswith(".gif"):
        #         mimetype='image/gif'
        #         sendReply = True
        #     if self.path.endswith(".js"):
        #         mimetype='application/javascript'
        #         sendReply = True
        #     if self.path.endswith(".css"):
        #         mimetype='text/css'
        #         sendReply = True
        #
        #     if sendReply == True:
        #         #Open the static file requested and send it
        #         f = open(curdir + sep + self.path)
        #         self.send_response(200)
        #         self.send_header('Content-type',mimetype)
        #         self.end_headers()
        #         self.wfile.write(f.read())
        #         f.close()
        #     return

        # except IOError:
        # self.send_error(404,'File Not Found: %s' % self.path)


if __name__ == '__main__':
    try:
        lock = threading.Lock()
        server_plugin(lock)
        while True:
            pass
    except KeyboardInterrupt:
        print '\nexiting via KeyboardInterrupt'

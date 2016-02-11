import socket
import json
import time
import threading
import thread
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

PORT_NUMBER = 80

class server_plugin(threading.Thread):


    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.daemon = True
        self.start()

    def run(self):

        #Create a web server and define the handler to manage the
        #incoming request

        try:
            self.server = HTTPServer(('', PORT_NUMBER), web_server_handler)
            self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.lock.acquire()
            print 'Started httpserver on port ' , PORT_NUMBER
            self.lock.release()
            #Wait forever for incoming htto requests
            self.server.serve_forever()

        except KeyboardInterrupt, IOError:
            self.tear_down()


    def tear_down(self):
        self.server.socket.close()
        self.server.shutdown()

class web_server_handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_error(404,'File Not Found: %s' % self.path)

        client_url = self.path
        client_ip = self.client_address # ip and port
        request_time = time.strftime("%H:%M:%S")

        json_data = {'clientData': {'clientIP': client_ip,
                                    'clientURL': client_url},
                     'dateRequestedTime': request_time}

        # export to db or something here
        print(json.dumps(json_data))


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

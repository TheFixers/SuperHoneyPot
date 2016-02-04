'''
To use currently, you need to run this .py
In a browser https://localhost:4443/

Need set a fakewebsite up and get recording to working
It will already multithread.
'''



import BaseHTTPServer, SimpleHTTPServer
import ssl
#from UnitTestFolder import certificate.crt

httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='server.pem', server_side=True)
httpd.serve_forever()
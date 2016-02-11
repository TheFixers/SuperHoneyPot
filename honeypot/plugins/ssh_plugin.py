## www.github.com/paramiko/paramiko
## and  docs.python.org/2/library/socket.html

import datetime
import sys
import socket
import threading
import json
import paramiko
import paramiko.transport
import os

currentFilePath = os.path.dirname(os.path.realpath(__file__))
host_key = paramiko.RSAKey(filename=currentFilePath + os.path.sep + 'randomKey.key')

isStarted = False

class server_plugin(paramiko.ServerInterface):

    PORT = 22
    sshSocket = None
    client = None
    address = None
    server = None
    channel = None

    def __init__(self, lock):
        self.lock = lock
        self.PortNumber = 22
        self.run()
        self.event = threading.Event()

    def check_auth_none(self, username):
        return paramiko.AUTH_SUCCESSFUL

print('SSH LOADED')
## sets up a socket and begins listening for connection requests
try:
    sshSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sshSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sshSocket.bind(('', 22))
except Exception as e:
    print('Bind failure: ' + str(e))

try:
    sshSocket.listen(10)
    print('Listening on port 22...' )
    ## accepts a connection request from the client and records the client info
    client, address = sshSocket.accept()
    time = datetime.datetime.now().time()
except Exception as e:
    print('Connection failure: ' + str(e))

try:
    DoGSSAPIKeyExchange = True
    print('Connection attempting...')
    t = paramiko.Transport(client)
    print('1')

    try:
        t.load_server_moduli()
    except:
        print('(Failed to load moduli -- gex will be unsupported.)')
        raise
    print('2')
    t.add_server_key(host_key)
    print('3')
    server = server_plugin()
    print('complete. Starting server')
    try:
        t.start_server(server=server)
        print('4')
    except paramiko.SSHException:
        print('*** SSH negotiation failed.')
    channel = t.accept(15)
    if channel is None:
        print('*** No channel.')
        sys.exit(1)
    print('Authenticated!')
    channel.send('Username: ')
    temp = channel.makefile('name')
    client_username = temp.readline().strip('\r\n')
    channel.send('Password: ')
    temp = channel.makefile('pass')
    client_password = temp.readline().strip('\r\n')
    t.close()

    clientIP = sshSocket.getpeername()

    json_data = {'ssh_data': {'clientIP': clientIP, 'client_port': PORT,
                              'username': client_username, 'password': client_password},
                 'connection_time': time}
    print(json.dumps(json_data))

except Exception as e:
    print('Failure to complete connection: ' + str(e))
    try:
        t.close()
    except:
        pass

            #self.teardown()

    def teardown(self):
        self.sshSocket.shutdown()
        self.sshSocket.close()

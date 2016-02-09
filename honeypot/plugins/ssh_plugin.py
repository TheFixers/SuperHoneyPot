## www.github.com/paramiko/paramiko
## and  docs.python.org/2/library/socket.html

import datetime
import sys
import socket
import threading
import json
import paramiko
import os

currentFilePath = os.path.dirname(os.path.realpath(__file__))
host_key = paramiko.RSAKey(filename = currentFilePath + os.path.sep + 'randomKey.key')


class server_plugin(paramiko.ServerInterface):

    PORT = 22

    def __init__(self, lock):
        self.lock = lock
        self.PortNumber = 22
        self.run()

    def check_auth_none(self, username):
        return paramiko.AUTH_SUCCESSFUL

    def testLoaded(self):
        print('SSH LOADED')

    def run(self):
        euid = os.geteuid()
        if euid != 0:
            print('Running sudo...')
            args = ['sudo', sys.executable] + sys.argv + [os.environ]
            os.execlpe('sudo', *args)
            ## sets up a socket and begins listening for connection requests
            try:
                sshSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sshSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sshSocket.bind(('', 3333))
            except Exception as e:
                print('Bind failure: ' + str(e))

            try:
                sshSocket.listen(10)
                print('Listening on ' )
                ## accepts a connection request from the client and records the client info
                client, address = sshSocket.accept()
                time = datetime.datetime.now().time()
            except Exception as e:
                print('Connection failure: ' + str(e))

            DoGSSAPIKeyExchange = True

            try:
                print('Connection attempting...')
                t = paramiko.Transport(client, gss_kex=DoGSSAPIKeyExchange)
                t.set_gss_host(socket.getfqdn(""))
                try:
                    t.load_server_moduli()
                except:
                    print('(Failed to load moduli -- gex will be unsupported.)')
                    raise
                t.add_server_key(host_key)
                server = ssh_plugin()
                try:
                    t.start_server(server=server)
                except paramiko.SSHException:
                    print('*** SSH negotiation failed.')
                channel = t.accept(15)
                channel.send('Username: ')
                temp = channel.makefile('name')
                client_username = temp.readline().strip('\r\n')
                channel.send('Password: ')
                temp = channel.makefile('pass')
                client_password = temp.readline().strip('\r\n')
                t.close()

                clientIP = sshSocket.getpeername()

                json_data = {'ssh_data': {'clientIP': clientIP, 'client_port': self.PORT,
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

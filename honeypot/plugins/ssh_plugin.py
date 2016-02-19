## www.github.com/paramiko/paramiko
## and  docs.python.org/2/library/socket.html

import datetime
import sys
import socket
import threading
import json

from binascii import hexlify

import paramiko
from paramiko.py3compat import b, u, decodebytes
import os

# setup logging
paramiko.util.log_to_file('demo_server.log')

currentFilePath = os.path.dirname(os.path.realpath(__file__))
host_key = paramiko.RSAKey(filename=currentFilePath + os.path.sep + 'randomKey.key')

isStarted = False

class server_plugin(paramiko.ServerInterface, threading.Thread):
    PORT = 22
    sshSocket = None
    client = None
    address = None
    server = None
    channel = None
    pulledKey = None

    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.daemon = True
        self.event = threading.Event()
        self.start()

    def get_ssh_socket(self):
        try:
            ssh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssh_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ssh_socket.bind(('', 22))

            return ssh_socket
        except Exception as e:
            print('Bind failure: ' + str(e))

    def accept(self):
        try:

            ssh_socket = self.get_ssh_socket()
            ssh_socket.listen(100)
            self.lock.acquire()
            print 'Started ssh on port 22'
            self.lock.release()
            ## accepts a connection request from the client and records the client info
            client, address = ssh_socket.accept()
            time = datetime.datetime.now().time()

            return client, address, time

        except Exception as e:
            print('Connection failure: ' + str(e))


    def run(self):
        self.lock.acquire()
        print('SSH LOADED')
        self.lock.release()
        ## sets up a socket and begins listening for connection requests
        try:
            client, address, time = self.accept()
            self.lock.acquire()
            self.lock.release()
            DoGSSAPIKeyExchange = True
            print('ssh connection attempting...')
            t = paramiko.Transport(client, gss_kex=False)
            t.set_gss_host(socket.getfqdn(""))
            try:
                t.load_server_moduli()
            except:
                print('(Failed to load moduli -- gex will be unsupported.)')
                raise
            t.add_server_key(host_key)
            server = server_plugin(self.lock)
            #print('Captured IP is: ' + self.pulledKey)
            print('complete. Starting server')
            try:
                t.start_server(server=server)
                print('4')
            except paramiko.SSHException:
                print('*** SSH negotiation failed.')
            channel = t.accept(20)
            if channel is None:
                print('*** No channel.')
                sys.exit(1)
#            print('Authenticated!')
#            channel.send('Username: ')
#            temp = channel.makefile('name')
#            client_username = temp.readline().strip('\r\n')
#            channel.send('Password: ')
#            temp = channel.makefile('pass')
#            client_password = temp.readline().strip('\r\n')
#            channel.close()
        except Exception as e:
            print('Failure to complete connection: ' + str(e))
            try:
                t.close()
            except:
                pass

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'robey') and (password == 'foo'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
        self.pulledKey = u(hexlify(key.get_fingerprint()))
        if (username == 'robey') and (key == self.good_pub_key):
            return paramiko.AUTH_FAILED   ##(default: paramiko.AUTH-SUCCESSFUL)
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_with_mic(self, username,
                                   gss_authenticated=paramiko.AUTH_FAILED,
                                   cc_file=None):
        """
        .. note::
            We are just checking in `AuthHandler` that the given user is a
            valid krb5 principal! We don't check if the krb5 principal is
            allowed to log in on the server, because there is no way to do that
            in python. So if you develop your own SSH server with paramiko for
            a certain platform like Linux, you should call ``krb5_kuserok()`` in
            your local kerberos library to make sure that the krb5_principal
            has an account on the server and is allowed to log in as a user.
        .. seealso::
            `krb5_kuserok() man page
            <http://www.unix.com/man-page/all/3/krb5_kuserok/>`_
        """
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_keyex(self, username,
                                gss_authenticated=paramiko.AUTH_FAILED,
                                cc_file=None):
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        UseGSSAPI = True
        GSSAPICleanupCredentials = False
        return UseGSSAPI

    def get_allowed_auths(self, username):
        return 'gssapi-keyex,gssapi-with-mic,password,publickey'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True

if __name__ == '__main__':
    try:
        lock = threading.Lock()
        server_plugin(lock)
        while True:
            pass
    except KeyboardInterrupt:
        print '\nexiting via KeyboardInterrupt'









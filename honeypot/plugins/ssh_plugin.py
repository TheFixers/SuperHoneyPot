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

## www.github.com/paramiko/paramiko
## and  docs.python.org/2/library/socket.html

import datetime
import sys
import socket
import threading
import json
from binascii import hexlify
import paramiko
from paramiko.py3compat import b, u
import os
import honeypot_db_interface

# setup logging
paramiko.util.log_to_file('demo_server.log')

currentFilePath = os.path.dirname(os.path.realpath(__file__))
host_key = paramiko.RSAKey(filename=currentFilePath + os.path.sep + 'randomKey.key')


class server_plugin(paramiko.ServerInterface, threading.Thread):
    PORT = 22
    sshSocket = None
    client = None
    address = None
    time = None
    server = None
    channel = None
    pulledKey = None
    clientIP = None
    clientUsername = ''
    clientPassword = ''
    interface = honeypot_db_interface.honeypot_database_interface()

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
            ssh_socket.bind(('', server_plugin.PORT))
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
            server_plugin.time = datetime.datetime.now().time()
            server_plugin.clientIP = address[0]
            return client, address, server_plugin.time
        except Exception as e:
            print('Connection failure: ' + str(e))

    def run(self):
        self.lock.acquire()
        #print('SSH LOADED')
        self.lock.release()
        ## sets up a socket and begins listening for connection requests
        try:
            client, address, time = self.accept()
            self.lock.acquire()
            self.lock.release()
            #print('ssh connection attempting...')
            # creates the ssh transport over the socket
            t = paramiko.Transport(client, gss_kex=False)
            t.set_gss_host(socket.getfqdn(""))
            try:
                t.load_server_moduli()
            except:
                print('(Failed to load moduli -- gex will be unsupported.)')
                raise
            t.add_server_key(host_key)  # sets the server RSA key
            server = server_plugin(self.lock)
            #print('complete. Starting server')
            try:
                # starts a new ssh server session and opens a thread for
                # protocol negotiation.
                t.start_server(server=server)
            except paramiko.SSHException:
                print('*** SSH negotiation failed.')
            channel = t.accept(60)
            # Channel will always be none because the client cannot
            # authenticate to request a channel.
            if channel is None:
                #print('*** No channel.')
                return
        except Exception as e:
            print('Failure to complete connection: ' + str(e))
            try:
                t.close()
            except:
                pass
        self.lock.acquire()
        # Displays, sends, then clears collected data fields.
        self.display_output()
        self.send_output()
        self.clear_vars()
        self.lock.release()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # Performs username and password authentication. Captures username
        # and all password attempts, including empty strings.
        server_plugin.clientUsername = username
        if password == '':
            server_plugin.clientPassword += '<null> '
        else:
            server_plugin.clientPassword += (password + ' ')
        if (username == 'robey') and (password == 'foo'):
            return paramiko.AUTH_FAILED  # (default: paramiko.AUTH_SUCCESSFUL)
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        # Allows the user to submit a key for authentication,
        # if applicable, then captures the key
        server_plugin.pulledKey = u(hexlify(key.get_fingerprint()))
        #print('Auth attempt with key: ' + server_plugin.pulledKey)
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

    def display_output(self):
        # Server-side display string
        print('Attack: ' + server_plugin.time.__str__() + ' on port ' + server_plugin.PORT.__str__() + '.')
        '''
        # Prints out all captured data from the attacker
        print('Attack time: ' + server_plugin.time.__str__())
        print('Attacker key: ' + server_plugin.pulledKey)
        print('Attacker IP:  ' + server_plugin.clientIP)
        print('Port of incoming attack: ' + server_plugin.PORT.__str__())
        print('Submitted username: ' + server_plugin.clientUsername)
        print('Submitted password: ' + server_plugin.clientPassword)
        '''
        return

    def send_output(self):
        # creates an output string to be sent to the database (via interface)
        dump_string = json.dumps({'Client':{'IP':server_plugin.clientIP,'Port':server_plugin.PORT.__str__(),
                                            'Data':{'Time':server_plugin.time.__str__(),
                                                    'Username':server_plugin.clientUsername,
                                                    'Passwords':server_plugin.clientPassword,
                                                    'Key':server_plugin.pulledKey}}})
        #print(dump_string)
        server_plugin.interface.receive_data(dump_string)
        return

    def clear_vars(self):
        # clears out the variables in preparation for a new connection attempt
        server_plugin.time = None
        server_plugin.clientIP = None
        server_plugin.pulledKey = None
        server_plugin.clientUsername = ''
        server_plugin.clientPassword = ''
        return


if __name__ == '__main__':
    try:
        lock = threading.Lock()
        server_plugin(lock)
        while True:
            pass
    except KeyboardInterrupt:
        print '\nexiting via KeyboardInterrupt'

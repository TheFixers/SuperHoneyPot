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
import time


path = os.path.dirname(os.path.realpath(__file__)).replace("plugins", "db_interface")
sys.path.insert(0, path)

import honeypot_db_interface

private_key_filepath = os.path.dirname(os.path.realpath(__file__).replace("plugins", "data_files"))
host_key = paramiko.RSAKey(filename=private_key_filepath + os.path.sep + 'privateSSHKey.key')

HOST = ''

class server_plugin(threading.Thread):

    def __init__(self, lock, port):
        threading.Thread.__init__(self)
        self.port = int(float(port))
        self.lock = lock
        self.daemon = True
        self.event = threading.Event()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()

    def run(self):

        #Bind socket to local host and port
        try:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((HOST, self.port))
        except socket.error as msg:
            self.lock.acquire()
            print ERROR + 'Bind failed. ' + str(msg[0]) + ' Message ' + msg[1]
            self.lock.release()
            sys.exit()

        #Start listening on socket
        self.s.listen(4)
        self.lock.acquire()
        print 'Started ssh server on port ', self.port
        self.lock.release()

                #now keep talking with the client
        while 1:
            #wait to accept a connection - blocking call
            conn, addr = self.s.accept()  
            self.lock.acquire()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            self.lock.release()
            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            client_thread(conn, addr, self.lock, self.port)

        try:
            while True:
                pass
        except KeyboardInterrupt, IOError:
                self.tear_down()

    def tear_down(self):
        self.lock.acquire()
        print 'ssh '+str(self.port)+' closing'   
        self.lock.release()     
        self.s.close()

class client_thread(paramiko.ServerInterface, threading.Thread):

    client = None
    PORT = None
    address = None
    socket = None
    time = None
    server = None
    channel = None
    pulledKey = None
    clientIP = None
    clientUsername = ''
    clientPassword = ''
    interface = honeypot_db_interface.honeypot_database_interface()

    def __init__(self, conn, addr, lock, port):
        threading.Thread.__init__(self)
        self.lock = lock
        client_thread.client = conn
        client_thread.address = addr    # explination of (ip, port) in addr 
        client_thread.clientIP = addr[0]
        client_thread.PORT = port
        client_thread.socket = addr[1]  # http://stackoverflow.com/questions/12454675/whats-the-return-value-of-socket-accept-in-python
        client_thread.time = datetime.datetime.now().time()
        self.daemon = True
        self.start()

    def run(self):
        # sets up a socket and begins listening for connection requests
        try:

            # creates the ssh transport over the socket
            t = paramiko.Transport(client_thread.client, gss_kex=False)
            t.set_gss_host(socket.getfqdn(""))
            try:
                t.load_server_moduli()
            except:
                print('(Failed to load moduli -- gex will be unsupported.)')
                raise
            t.add_server_key(host_key)  # sets the server RSA key
            server = self

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
                pass
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
        self.lock.release()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # Performs username and password authentication. Captures username
        # and all password attempts, including empty strings.
        client_thread.clientUsername = username
        if password == '':
            client_thread.clientPassword += '<null> '
        else:
            client_thread.clientPassword += (password + ' ')
        if (username == 'robey') and (password == 'foo'):
            return paramiko.AUTH_FAILED  # (default: paramiko.AUTH_SUCCESSFUL)
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        # Allows the user to submit a key for authentication,
        # if applicable, then captures the key
        client_thread.pulledKey = u(hexlify(key.get_fingerprint()))
        #print('Auth attempt with key: ' + client_thread.pulledKey)
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
        print('SSH Attack: ' + client_thread.time.__str__() + ' from ' + client_thread.clientIP + ' on port ' + client_thread.PORT.__str__() + '.')
        '''
        # Prints out all captured data from the attacker
        print('Attack time: ' + client_thread.time.__str__())
        print('Attacker key: ' + client_thread.pulledKey)
        print('Attacker IP:  ' + client_thread.clientIP)
        print('Port of incoming attack: ' + client_thread.PORT.__str__())
        print('Submitted username: ' + client_thread.clientUsername)
        print('Submitted password: ' + client_thread.clientPassword)
        '''
        return

    def send_output(self):
        # creates an output string to be sent to the database (via interface)
        dump_string = json.dumps({'Client':{'TYPE':"SSH",'IP':client_thread.clientIP,'Port':client_thread.PORT.__str__(),'Socket':str(client_thread.socket),
                                            'Data':{'Time':client_thread.time.__str__(),
                                                    'Username':client_thread.clientUsername,
                                                    'Passwords':client_thread.clientPassword,
                                                    'Key':client_thread.pulledKey}}})
        #print(dump_string)
        client_thread.interface.receive_data(dump_string)
        return



if __name__ == '__main__':
    try:
        lock = threading.Lock()
        server_plugin(lock)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print '\nexiting via KeyboardInterrupt'

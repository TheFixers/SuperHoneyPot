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

import threading
import time
import sys
import re
import grp
import os
import pwd
import pluginsReader
import platform
# sets path for reading in .py files to plugins folder
path = os.path.dirname(os.path.realpath(__file__)).replace("honey_loader", "plugins")
sys.path.insert(0, path)

path = path.replace("plugins", "data_files")
text_file = open(path + os.path.sep + "plugins.txt", "r")
lines = re.split('\n| ', text_file.read())  # regex for new line and blanks
lock = None

def start_plugins():

    try:
        # Checks to see if program has root privileges and warns user if not
        if check_root() == 0:
            start()
        else:
            print("We never got root! exiting now")
            sys.exit(2)
    except EnvironmentError as e:
        print(str(e))


def start():
    lines = pluginsReader.lineReader()
    global lock
    plugins = []
    try:
        # Read through the plugin list and load them with the indicated ports
        lock = threading.Lock()
        for line in lines:
            plug = line.pop(0)          #first index is plugin name
            plugin = __import__(plug)
            for port in line:
                try: 
                    plugins.append(plugin.server_plugin(lock, port))
                except socket.error as msg:
                    print 'Plugin not opened on port, error.'
                     

        time.sleep(1)     # wait 1 second so last plugin has time to bind

        if os.name == 'posix' and platform.dist()[0] == '':
            drop_privileges_Arch()      # drops root privileges
        else:
            drop_privileges()

        while True:
            time.sleep(1)   # Keeps the program running until keyboard interrupt closes.
    except KeyboardInterrupt:
        lock.acquire()
        print '\nexiting via KeyboardInterrupt'
        for plugin in plugins:
            plugin.tear_down()    # Graceful closure of each plugin and its open sockets
        lock.release()
        sys.exit()
    except Exception as e:
        lock.acquire()
        print('ERROR: ' + str(e))
        for plugin in plugins:
            plugin.tear_down()
        lock.release()
        sys.exit()


def check_root():
    # check if plugins really need root. This is from plugins.txt file
    if lines[0] == "#root":
        # first check if program has root access
        if os.geteuid() == 0 or os.getegid() == 0:
            return 0
        else:
            raise EnvironmentError, "need to be root"
    else:
        return 0


def drop_privileges(uid_name="nobody", gid_name="nogroup"):
    if os.getuid() != 0:
        # Already not root, take no action
        return

    # Get the uid/gid from the name
    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(running_gid)
    os.setuid(running_uid)

    # Ensure a very conservative umask
    old_umask = os.umask(077)

def drop_privileges_Arch(uid_name="nobody", gid_name="nobody"):
    if os.getuid() != 0:
        # Already not root, take no action
        return

    # Get the uid/gid from the name
    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(running_gid)
    os.setuid(running_uid)

    # Ensure a very conservative umask
    old_umask = os.umask(077)

if __name__ == '__main__':
    start_plugins()

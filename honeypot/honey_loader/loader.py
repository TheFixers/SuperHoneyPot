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

# sets path for reading in .py files to plugins folder
path = os.path.dirname(os.path.realpath(__file__)).replace("honey_loader", "plugins")
sys.path.insert(0, path)

path = path.replace("plugins", "data_files")
text_file = open(path + os.path.sep + "plugins.txt", "r")
lines = re.split('\n| ', text_file.read())  # regex for new line and blanks
lock = None


def start_plugins():

    try:

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
    try:

        lock = threading.Lock()
        for line in lines:
            plug = line.pop(0)          #first index is plugin name
            plugin = __import__(plug)
            for port in line:
                plugin.server_plugin(lock, port)

        time.sleep(1)     # wait 1 second so last plugin has time to bind
        drop_privileges()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        lock.acquire()
        print '\nexiting via KeyboardInterrupt'
        lock.release()
        sys.exit()
    except Exception as e:
        lock.acquire()
        print('ERROR: ' + str(e))
        sys.exit()
        lock.release()


# Very experimental, doesn't work for all linux distros where root has no password (debian based os needs to do sudo su)
# Not sure how to check for this issue...

# def prompt_sudo():
#     ret = 0
#     if os.geteuid() != 0:
#         args = ['sudo', sys.executable] + sys.argv + [os.environ]
#     # the next line replaces the currently-running process with the sudo
#     os.execlpe('sudo', *args)
#     return ret and os.geteuid() == 0


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


def drop_privileges(uid_name="nobody", gid_name="nobody"):
    if os.getuid() != 0:
        # We're not root so, like, whatever dude
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

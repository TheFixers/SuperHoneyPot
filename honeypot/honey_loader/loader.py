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

import os
import threading
import time
import sys
import re

# sets path for reading in .py files to plugins folder
path = os.path.dirname(os.path.realpath(__file__)).replace("honey_loader", "plugins")
sys.path.insert(0, path)

path = path.replace("plugins", "")

text_file = open(path + "plugins.txt", "r")
lines = re.split('\n| ', text_file.read())  # regex for new line and blanks
lock = None


def start_plugins():
    global lock
    try:

        lock = threading.Lock()
        for i in lines:
            if i != '' and i[:1] != '#':  # ignore blank lines and comments starting with #
                plugin = __import__(i)
                plugin.server_plugin(lock)

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
        lock.release()
        sys.exit()


if __name__ == '__main__':
    start_plugins()

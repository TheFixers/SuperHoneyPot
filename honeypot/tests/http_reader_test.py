import os
import sys

path = os.path.dirname(os.path.realpath(__file__)).replace("tests", "plugins")
sys.path.insert(0, path)

import http_reader

http_reader.server_plugin()

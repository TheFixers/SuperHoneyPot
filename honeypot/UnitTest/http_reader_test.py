import os
path = os.path.dirname(os.path.realpath(__file__)).replace("UnitTest", "plugins")

import sys
sys.path.insert(0, path)

from http_reader import http_server_plugin, web_server_handler

server = http_server_plugin(8080)/
from src import telnet_reader
from src import http_reader
from src import https_reader


while 1:
    telnet_reader.Server(telnet_reader.s.accept()).start()
    https_reader.Server(https_reader.s.accept()).start()
    http_reader.Server(http_reader.s.accept()).start()

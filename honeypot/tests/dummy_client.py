import socket
import httplib



try:

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 8888))

except Exception as e:
    print e
finally:
    conn.close()
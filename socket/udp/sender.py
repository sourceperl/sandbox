"""
Basic periodic UDP sender.

"""

import socket
import time

# some const
UDP_IP = '127.0.0.1'
UDP_PORT = 7800


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        sock.sendto(f'timestamp is {time.time()}'.encode(), (UDP_IP, UDP_PORT))
        time.sleep(1)
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f'an error occur: {e}')
finally:
    sock.close()

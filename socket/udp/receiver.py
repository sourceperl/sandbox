"""
Basic UDP receiver.

"""

import socket


# some const
UDP_IP = '127.0.0.1'
UDP_PORT = 7800


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, address_t = sock.recvfrom(512)
        print(f'rx {len(data)} bytes from {address_t}: {data}')
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f'an error occur: {e}')
finally:
    sock.close()

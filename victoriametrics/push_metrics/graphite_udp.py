"""Push some metrics to VictoriaMetrics with graphite protocol over UDP.

https://docs.victoriametrics.com/#how-to-send-data-from-graphite-compatible-agents-such-as-statsd
"""

import socket


# some const
VM_IP = '127.0.0.1'
VM_PORT = 2003


# send message to VictoriaMetrics
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.sendto(b'my_metric;tag1=value1 42.0', (VM_IP, VM_PORT))
except socket.error as e:
    print(f'error occur: {e!r}')
finally:
    s.close()

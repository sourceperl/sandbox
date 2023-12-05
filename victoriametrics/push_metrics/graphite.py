"""Push some metrics to VictoriaMetrics with graphite protocol.

https://docs.victoriametrics.com/#how-to-send-data-from-graphite-compatible-agents-such-as-statsd
"""

import random
import socket
import time


# some const
VM_IP = '127.0.0.1'
VM_PORT = 2003

# main loop
while True:
    # define metric
    metric_name = 'tag_hist'
    metric_value = random.random()
    # define publish message
    pub_msg = f'{metric_name};tag=RAND_1 {metric_value}\n'.encode()
    pub_msg += f'{metric_name};tag=RAND_2 {metric_value}\n'.encode()
    print(f'publish {pub_msg}')
    # send message to VictoriaMetrics
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((VM_IP, VM_PORT))
        s.send(pub_msg)
    except socket.error as e:
        print(f'error occur: {e!r}')
    finally:
        s.close()
    # wait for next refresh
    time.sleep(1.0)

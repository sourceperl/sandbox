"""Push some metrics to VictoriaMetrics with prometheus text exposition format.

https://docs.victoriametrics.com/#how-to-import-data-in-prometheus-exposition-format
"""

import math
import random
import time
from urllib.request import Request, urlopen
from urllib.error import URLError


# some const
VM_WRITE_URL = 'http://127.0.0.1:8428/api/v1/import/prometheus'
METRIC_NAME = 'tag_hist'


# main loop
while True:
    # tags list
    tags_l = [('RANDOM', random.random()), ('SIN', math.sin(2*math.pi*time.time()))]
    # format line protocol message
    prom_txt_msg = ''
    for tag_name, value in tags_l:
        # here time series names correspond to field names
        prom_txt_msg += f'{METRIC_NAME}{{tag="{tag_name}"}} {value}\n'
    # post message to VictoriaMerctrics
    try:
        prom_txt_msg_b = prom_txt_msg.encode()
        urlopen(Request(url=VM_WRITE_URL, data=prom_txt_msg_b), timeout=4.0)
        print(f'POST {len(prom_txt_msg_b)} bytes OK')
    except URLError as e:
        print(f'error occur: {e!r}')
    # wait for next refresh
    time.sleep(1.0)

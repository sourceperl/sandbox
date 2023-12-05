"""Push some metrics to VictoriaMetrics with line protocol (influxdb).

https://docs.victoriametrics.com/#how-to-send-data-from-influxdb-compatible-agents-such-as-telegraf
"""

import math
import random
import time
from urllib.request import Request, urlopen
from urllib.error import URLError


# some const
VM_WRITE_URL = 'http://127.0.0.1:8428/write'
METRIC_NAME = 'tag_hist'


# main loop
while True:
    # tags list
    tags_l = [('RANDOM', random.random()), ('SIN', math.sin(2*math.pi*time.time()))]
    # format line protocol message
    line_msg = ''
    for tag_name, value in tags_l:
        # here time series names correspond to field names
        line_msg += f',tag={tag_name} {METRIC_NAME}={value}\n'
    # post message to VictoriaMerctrics
    try:
        urlopen(Request(url=VM_WRITE_URL, data=line_msg.encode()), timeout=4.0)
    except URLError as e:
        print(f'error occur: {e!r}')
    # wait for next refresh
    time.sleep(1.0)

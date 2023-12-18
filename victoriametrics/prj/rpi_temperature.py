""" Post Raspberry PI CPU temperature to VictoriaMetrics. """

import time
from urllib.request import Request, urlopen
from urllib.error import URLError


# some const
VM_WRITE_URL = 'http://127.0.0.1:8428/api/v1/import/prometheus'
METRIC_NAME = 'rpi_cpu_temp'


# main loop
while True:
    # post to VictoriaMerctrics
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            cpu_temp = float(f.read()) / 1000
        prom_txt_msg_b = f'{METRIC_NAME} {cpu_temp}\n'.encode()
        urlopen(Request(url=VM_WRITE_URL, data=prom_txt_msg_b), timeout=4.0)
        print(f'POST {prom_txt_msg_b} OK')
    except URLError as e:
        print(f'error occur: {e!r}')
    # wait for next refresh
    time.sleep(1.0)

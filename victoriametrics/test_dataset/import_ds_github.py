""" Fetch a dataset from github.

- Publish it to VictoriaMetrics graphite endpoint for further test prupose
- Add a timestamp offset to avoid VM skip data outside of retention period
"""

import csv
from datetime import datetime, timezone
import socket
from urllib.request import urlopen


# some const
CSV_URL = 'https://raw.githubusercontent.com/numenta/NAB/v1.1/data/artificialWithAnomaly/art_daily_flatmiddle.csv'
VM_METRIC = 'my_github_metric'
VM_IP = '127.0.0.1'
VM_PORT = 2003


# request CSV data from github
csv_data_str = urlopen(CSV_URL).read().decode()
csv_as_lines_l = csv_data_str.splitlines()

# format CSV data for publication
vm_stamp_l, vm_value_l = [], []
for row in csv.DictReader(csv_as_lines_l, delimiter=','):
    # convert row timestamp and value fields to VictoriaMetrics format
    vm_stamp_l.append(round(datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S').timestamp()))
    vm_value_l.append(float(row['value']))

# ensure top timestamp in dataset match current UTC timestamp (avoid VM skip outside retention data)
now_ts = datetime.now(timezone.utc).timestamp()
ts_offset = now_ts - max(vm_stamp_l)
vm_stamp_l = [x + ts_offset for x in vm_stamp_l]

# format publication message
pub_msg = ''
for vm_value, vm_stamp in zip(vm_value_l, vm_stamp_l):
    # add new line to publication message (format: "metric value timestamp\n")
    pub_msg += (f'{VM_METRIC} {vm_value} {vm_stamp}\n')

# send message to VictoriaMetrics on graphite endpoint
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((VM_IP, VM_PORT))
    s.send(pub_msg.encode())
    print(f'publish {len(pub_msg)} bytes OK')
except socket.error as e:
    print(f'error occur: {e!r}')
finally:
    s.close()

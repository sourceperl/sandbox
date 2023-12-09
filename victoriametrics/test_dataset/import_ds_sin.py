""" Build a one hour dataset with a noisy sin value.

- Publish it to VictoriaMetrics import endpoint as a json message
"""

from datetime import datetime, timezone
import json
from math import pi, sin
import random
from urllib.request import Request, urlopen
from urllib.error import URLError


# some const
VM_API_URL = 'http://127.0.0.1:8428/api/v1'
VM_IMPORT_URL = VM_API_URL + '/import'
VM_METRIC = 'my_sin_metric'

# purge old values
#urlopen(f'{VM_API_URL}/admin/tsdb/delete_series?match[]={VM_METRIC}')

# ensure top timestamp in dataset match current UTC timestamp (avoid VM skip outside retention data)
now_ts = round(datetime.now(timezone.utc).timestamp())

vm_value_l, vm_stamp_l = [], []
for ts in  range(now_ts - 3600, now_ts):
    vm_stamp_l.append(ts*1_000)
    vm_value_l.append(sin(2*pi*ts*0.001) + 0.2 * random.random())

# format publication message as a compact json message
pub_json = json.dumps({'metric': {'__name__': VM_METRIC}, 'values': vm_value_l, 'timestamps': vm_stamp_l}, separators=(',', ':'))

# post message to VictoriaMerctrics
try:
    urlopen(Request(url=VM_IMPORT_URL, data=pub_json.encode()), timeout=4.0)
    print(f'import {len(pub_json)} bytes OK')
except URLError as e:
    print(f'error occur: {e!r}')

""" Decoded instant query range on VictoriaMetrics DB. """

from datetime import datetime
import json
from json.decoder import JSONDecodeError
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError


# some const
VM_QUERY_URL = 'http://127.0.0.1:8428/api/v1/query'
VM_METRIC = 'my_metric'

# format URL for query instant (until 1 hour from now)
q_params = urlencode(dict(query=VM_METRIC, step='2m'))
url = f'{VM_QUERY_URL}?{q_params}'

# send query to VictoriaMerctrics
try:
    # request
    with urlopen(url, timeout=4.0) as response:
        js_msg = response.read()
    # decode response
    js_d = json.loads(js_msg)
    if js_d['status'] == 'success':
        for result_d in js_d['data']['result']:
            ts, value = result_d['value']
            dt = datetime.fromtimestamp(ts)
            print(f"{result_d['metric']} {dt} {value}")
except (URLError, JSONDecodeError) as e:
    print(f'error occur: {e!r}')

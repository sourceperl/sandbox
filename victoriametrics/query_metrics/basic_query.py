""" Basic instant query on VictoriaMetrics DB. """

from pprint import pprint
import json
from json.decoder import JSONDecodeError
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError


# some const
VM_QUERY_URL = 'http://127.0.0.1:8428/api/v1/query'
VM_METRIC = 'my_metric'

# format URL for query instant (until 1 hour from now)
query_params = urlencode(dict(query=VM_METRIC, step='1h'))
url = f'{VM_QUERY_URL}?{query_params}'

# send query to VictoriaMerctrics
try:
    with urlopen(url, timeout=4.0) as response:
        js_msg = response.read()
    pprint(json.loads(js_msg))
except (URLError, JSONDecodeError) as e:
    print(f'error occur: {e!r}')

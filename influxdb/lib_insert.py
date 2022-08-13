#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sys
import time
import traceback
from influxdb import InfluxDBClient

# connect to influxdb DB
client = InfluxDBClient(host="localhost", port=8086)
client.switch_database("mydb")

while True:
    try:
        # update metrics
        l_metrics = [
            {
                "measurement": "test",
                "fields": {
                    "field1": random.randint(0, 100),
                    "field2": random.randint(0, 100),
                },
            },
        ]
        client.write_points(points=l_metrics)
        # wait for next update
        time.sleep(2.0)
    except KeyboardInterrupt:
        break
    except:
        # log except to stderr
        traceback.print_exc(file=sys.stderr)
        # wait before next try
        time.sleep(2.0)

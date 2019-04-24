#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient

# connect to influxdb DB
client = InfluxDBClient(host="localhost", port=8086)
client.switch_database("mydb")

# request for select last 3 records of "field1" in "test" measurement (mean value by 10s steps)
req = "SELECT mean(\"field1\") AS f1 FROM \"test\" GROUP BY time(10s) ORDER BY time DESC LIMIT 3"

# display data
for point in client.query(req).get_points():
    print(point)

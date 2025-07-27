#!/usr/bin/env python3

"""
Basic example of transferring metrics from influxdb to VictoriaMetrics with csv file.

# how to extract data on influxdb part
influx -database mydb -execute "SELECT * FROM ble_sensors" -format csv > output.csv
"""


import csv
import socket

# params
TEST_MODE = True


# some class
class VM:
    """A class to push metrics on VM with graphite UDP message."""

    IP = '127.0.0.1'
    PORT = 2003

    def __init__(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def push(self, msg: str):
        """Push a txt message to VM DB (example vm.push('my_metric;tag1=value1 42.0 1753600989'))"""
        try:
            self._sock.sendto(msg.encode(), (VM.IP, VM.PORT))
        except Exception as e:
            print(f'error occur: {e!r}')


# inits
vm = VM()
csvfile = open('output.csv', 'r')
sensors_allowed = ['bedroom', 'cellar', 'garage', 'kitchen', 'outdoor']

# process CSV rows
for row in csv.DictReader(csvfile):
    # process csv fields for current row
    measurement_name = str(row['name'])
    sensor = str(row['sensor'])
    # influxDB often stores timestamps in nanoseconds
    # 1753542768000000000 nanoseconds = 1753542768.0 seconds
    timestamp_ns = int(row['time'])
    timestamp_s = round(timestamp_ns / 1_000_000_000.0)
    # convert numeric fields to their appropriate types
    try:
        temp_c = float(row['temp_c'])
    except ValueError:
        temp_c = None
    try:
        hum_p = int(row['hum_p'])
    except ValueError:
        hum_p = None
    try:
        rssi = int(row['rssi'])
    except ValueError:
        rssi = None

    if sensor in sensors_allowed:
        graphite_txt = ''
        graphite_txt += f'ble_sensors_temperature_celsius;sensor={sensor} {temp_c} {timestamp_s}\n'
        graphite_txt += f'ble_sensors_humidity_percent;sensor={sensor} {hum_p} {timestamp_s}\n'
        graphite_txt += f'ble_sensors_rssi_dbm;sensor={sensor} {rssi} {timestamp_s}'

        print(f'push {graphite_txt.strip()!r}')
        if not TEST_MODE:
            vm.push(graphite_txt)

#!/usr/bin/env python3

""" Collect ThermoPro TP357 bluetooth data (https://buythermopro.com/product/tp357/). """

import logging
import os
import time
from struct import unpack
import sys
from bluepy.btle import Scanner, DefaultDelegate, ScanEntry


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        # extract device name
        short_name = dev.getValue(ScanEntry.SHORT_LOCAL_NAME) or ''
        # for TP357 ThermoPro Thermometer/Hygrometer
        if short_name.startswith('TP357'):
            # search manufacturer data (data type 0xff)
            manu_data = dev.getValue(0xff)
            if manu_data and len(manu_data) > 5:
                # extract temperature and humidity from manufacturer data
                (temp, hum) = unpack('<hB', manu_data[1:4])
                temp /= 10
                logging.info(f'from TP357 [{dev.addr}]: temperature is {temp:0.1f}°C, humidity is {hum}%')


if __name__ == '__main__':
    # root is need for doing a BLE scan
    if os.geteuid() != 0:
        sys.exit('BLE scan need to be run by root')

    # logging setup
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    # start BLE scan
    while True:
        try:
            Scanner().withDelegate(ScanDelegate()).scan(timeout=None, passive=True)
        except Exception as e:
            print(f'exception occur: {e}')
            time.sleep(1.0)

#!/usr/bin/env python3

""" Collect bluetooth low energy raw data. """

import logging
import os
import time
import sys
from bluepy.btle import Scanner, DefaultDelegate, ScanEntry


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev: ScanEntry, isNewDev: bool, isNewData: bool):
        # limit to nearby devices
        if dev.rssi > -70:
            data_l = dev.getScanData()
            logging.info(f'@{dev.addr} [{dev.rssi} dBm] {data_l}')


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
            logging.error(f'exception occur: {e}')
            time.sleep(1.0)

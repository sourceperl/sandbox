#!/usr/bin/env python3

import asyncio
# sudo pip3 install bleak
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


def on_advert(device: BLEDevice, adv_data: AdvertisementData):
    # monitor nearby advertisers
    if adv_data.rssi > -65:
        print(f'{device} {adv_data}')


async def main():
    # do BLE scan
    ble_scan = BleakScanner(detection_callback=on_advert)
    await ble_scan.start()
    while True:
        await asyncio.sleep(10)

asyncio.run(main())

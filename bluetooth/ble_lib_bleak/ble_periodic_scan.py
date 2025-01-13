#!/usr/bin/env python3

import asyncio

# sudo pip3 install bleak==0.22.3
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


def ble_detection_callback(device: BLEDevice, adv_data: AdvertisementData):
    print(f'[addr {device.address}] {adv_data!r}')


async def ble_task():
    scanner = BleakScanner(ble_detection_callback, scanning_mode='active')
    while True:
        # scan for 10 seconds
        await scanner.start()
        await asyncio.sleep(10)
        await scanner.stop()
        # 50 seconds break
        await asyncio.sleep(50)


loop = asyncio.get_event_loop()
loop.create_task(ble_task())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

#!/usr/bin/env python3

import asyncio
# sudo pip3 install bleak
from bleak import BleakScanner


async def main():
    # do BLE scan
    devices_d = await BleakScanner.discover(timeout=4.0, return_adv=True)
    # show results
    for addr, (ble_device, adv_data) in devices_d.items():
        print('-'*120)
        print(f'{addr=}')
        print(f'{ble_device=}')
        print(f'{adv_data=}')


asyncio.run(main())

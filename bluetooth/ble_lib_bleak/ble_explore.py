#!/usr/bin/env python3

import asyncio
# sudo pip3 install bleak
from bleak import BleakClient
from bleak.exc import BleakError
from private_data import BLE_DEV_ADDR


async def main():
    try:
        async with BleakClient(BLE_DEV_ADDR) as client:
            # show services available on BLE client
            print(f'explore services at {BLE_DEV_ADDR}:')
            for service in client.services:
                print(f'{service}')
                for char in service.characteristics:
                    print(f'\t{char}')
    except BleakError as e:
        print(f'BLE error occur: {e}')

asyncio.run(main())

#!/usr/bin/env python3

import asyncio
# sudo pip3 install bleak
from bleak import BleakClient
from bleak.exc import BleakError
from bleak.uuids import normalize_uuid_str
from private_data import BLE_DEV_ADDR


async def main():
    try:
        # disconnect from client on with exit
        async with BleakClient(BLE_DEV_ADDR) as client:
            # read temperature characteristic
            temp_raw = await client.read_gatt_char(normalize_uuid_str('2a6e'))
            # decode raw data and show it
            temp = int.from_bytes(temp_raw, byteorder='little', signed=True) / 100
            print(f'temperature value: {temp} °C')
    except BleakError as e:
        print(f'BLE error occur: {e}')

asyncio.run(main())

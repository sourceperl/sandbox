#!/usr/bin/env python3

""" A tool to inject modbus test frame on serial line (RS-485). """

import argparse
from datetime import datetime, timedelta
import logging
import struct
import sys
import time
# sudo pip install pyserial==3.4
from serial import Serial, serialutil


# some consts
FLX_ORIGIN_DT = datetime(year=1976, month=1, day=1)


# some functions
def crc16(frame: bytes):
    """Compute CRC16.

    :param frame: frame
    :type frame: bytes
    :returns: CRC16
    :rtype: int
    """
    crc = 0xFFFF
    for next_byte in frame:
        crc ^= next_byte
        for _ in range(8):
            lsb = crc & 1
            crc >>= 1
            if lsb:
                crc ^= 0xA001
    return crc


# some class
class FakeSerial:
    def __init__(self, **_) -> None:
        pass

    def write(self, data: bytes):
        print(data.hex(':'))


class ModbusSerialWorker:
    """ A worker to manage I/O with serial port. """

    def __init__(self, port: Serial):
        # args
        self.serial_port = port
        # tags bank
        self.hourly_station_d = (('VNHN', 800_000.0), ('EHN', 0.0), ('GCVHN', 0.0), ('PHN', 0.0), ('THN', 0.0),
                                 ('DHN', 0.0), ('RDHN', 0.0), ('N2HN', 0.0), ('CO2HN', 0.0),
                                 ('C1HN', 0.0), ('C2HN', 0.0), ('C3HN', 0.0), ('IC4HN', 0.0), ('NC4HN', 0.0),
                                 ('IC5HN', 0.0), ('NC5HN', 0.0), ('C6PHN', 0.0), ('GCVHMI', 0.0), ('GCVHMA', 0.0),
                                 ('MIAHN', 0.0), ('MIBHN', 0.0))
        self.daily_station_d = (('VNDN', 800_000.0), ('EDN', 0.0), ('VNFDN', 0.0), ('VNFADN', 0.0), ('VNRDN', 0.0),
                                ('VNRADN', 0.0), ('EFDN', 0.0), ('EFADN', 0.0), ('ERDN', 0.0), ('ERADN', 0.0))

    def flx_hourly_station_data(self):
        # format request frame
        slave_addr = 7
        func_code = 0x64
        hour_dt = datetime(year=2023, month=10, day=25, hour=14)
        hour_id = round((hour_dt - FLX_ORIGIN_DT).total_seconds()/3600)
        byte_qty = 0xf0
        request_frame = struct.pack('>BBIB', slave_addr, func_code, hour_id, byte_qty)
        # add CRC
        request_frame += struct.pack('<H', crc16(request_frame))
        # send request
        self.serial_port.write(request_frame)
        # add delay between request/reponse
        time.sleep(0.05)
        # format response frame
        byte_qty = 0xf0
        # build response frame
        # header
        response_frame = struct.pack('>BBB', slave_addr, func_code, byte_qty)
        # populate with tags and values
        for tag_name, tag_value in self.hourly_station_d:
            response_frame += f'{tag_name:<6s}'.encode() + struct.pack('>f', tag_value)
        # add 30 null bytes
        response_frame += bytes(30)
        # add CRC
        response_frame += struct.pack('<H', crc16(response_frame))
        # send response
        self.serial_port.write(response_frame)
        # add delay between request/reponse
        time.sleep(0.05)

    def flx_daily_station_data(self):
        # format request frame
        slave_addr = 7
        func_code = 0x65
        day_dt = datetime(year=2023, month=10, day=25)
        day_id = round((day_dt - FLX_ORIGIN_DT).total_seconds() / 86_400)
        byte_qty = 0xf0
        request_frame = struct.pack('>BBIB', slave_addr, func_code, day_id, byte_qty)
        # add CRC
        request_frame += struct.pack('<H', crc16(request_frame))
        # send request
        self.serial_port.write(request_frame)
        # add delay between request/reponse
        time.sleep(0.05)
        # format response frame
        byte_qty = 0xfd
        # build response frame
        # header
        response_frame = struct.pack('>BBB', slave_addr, func_code, byte_qty)
        # populate with tags and values
        for tag_name, tag_value in self.daily_station_d:
            response_frame += f'{tag_name:<6s}'.encode() + struct.pack('>f', tag_value)
        # add 140 null bytes
        response_frame += bytes(140)
        # add CRC
        response_frame += struct.pack('<H', crc16(response_frame))
        # send response
        self.serial_port.write(response_frame)
        # add delay between request/reponse
        time.sleep(0.05)

    def loop(self):
        """ Serial worker main loop. """
        # main loop
        while True:
            # hourly station data
            self.flx_hourly_station_data()
            # daily station data
            self.flx_daily_station_data()
            # delay before next cycle
            time.sleep(1.0)


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('device', type=str, help='serial device (like /dev/ttyUSB0)')
    parser.add_argument('-b', '--baudrate', type=int, default=9600, help='serial rate (default is 9600)')
    parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
    args = parser.parse_args()
    # init logging
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger(__name__)
    try:
        # init serial port
        logger.info(f'start serial modbus simulator {args.device}')
        serial_port = Serial(port=args.device, baudrate=args.baudrate)
        # init serial worker
        serial_worker = ModbusSerialWorker(port=serial_port)
        serial_worker.loop()
    except serialutil.SerialException as e:
        logger.error(f'serial device error: {e:r}')
        exit(1)

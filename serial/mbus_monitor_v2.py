#!/usr/bin/env python3

""" Modbus serial monitor """

import argparse
from dataclasses import dataclass
import logging
import sys
# sudo pip install pyserial==3.4
from serial import Serial, serialutil


# data
@dataclass
class FrameInfo:
    number: int = 0
    crc_ok: int = 0
    crc_err: int = 0


# some functions
def crc16(frame: bytes):
    """Compute CRC16.

    :param frame: frame
    :type frame: bytes
    :returns: CRC16
    :rtype: int
    """
    crc = 0xFFFF
    for item in frame:
        next_byte = item
        crc ^= next_byte
        for _ in range(8):
            lsb = crc & 1
            crc >>= 1
            if lsb:
                crc ^= 0xA001
    return crc


class ModbusSerialWorker:
    """ A serial worker to manage I/O with RTU devices. """

    def __init__(self, port: Serial, eof_ms=50.0):
        # public
        self.serial_port = port
        self.eof_ms = eof_ms
        self.frame_info = FrameInfo()

    def loop(self):
        """ Serial worker main loop. """
        # flush rx buffer
        self.serial_port.reset_input_buffer()
        # receive loop
        while True:
            # wait for first byte of frame
            self.serial_port.timeout = None
            rx_raw = self.serial_port.read(1)
            # if ok, wait for the remaining
            if rx_raw:
                # wait for next bytes of data until end of frame delay
                self.serial_port.timeout = self.eof_ms / 1000
                while True:
                    rx_chunk = self.serial_port.read(1)
                    if rx_chunk:
                        rx_raw += rx_chunk
                        # limit size to 256 bytes
                        rx_raw = rx_raw[-256:]
                    else:
                        break
                # call frame handler
                self.on_frame_detect(rx_raw)

    def on_frame_detect(self, frame: bytes):
        # check CRC
        crc_ok = crc16(frame) == 0
        crc_status = 'OK' if crc_ok else 'ERROR'
        # update FrameInfo struct
        self.frame_info.number += 1
        if crc_ok:
            self.frame_info.crc_ok += 1
        else:
            self.frame_info.crc_err += 1
        # log frame data
        logging.info(f"[{self.frame_info.number:6}] CRC: {crc_status:5} RAW: [{len(frame):3}] {frame.hex(':')[:23]}")


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('device', type=str, help='serial device (like /dev/ttyUSB0)')
    parser.add_argument('-b', '--baudrate', type=int, default=9600, help='serial rate (default is 9600)')
    parser.add_argument('-e', '--eof_ms', type=float, default=6.0, help='end of frame delay (default is 6 ms)')
    parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
    args = parser.parse_args()
    # init logging
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger(__name__)
    try:
        # init serial port
        logger.debug('Monitor serial port %s at %d bauds (eof = %.3f ms)',
                     args.device, args.baudrate, args.eof_ms)
        serial_port = Serial(port=args.device, baudrate=args.baudrate)
        # init serial worker
        serial_worker = ModbusSerialWorker(port=serial_port, eof_ms=args.eof_ms)
        serial_worker.loop()
    except serialutil.SerialException as e:
        logger.critical('Serial device error: %r', e)
        exit(1)

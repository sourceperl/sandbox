#!/usr/bin/env python3

""" Modbus serial monitor, relay frames to a redis channel. """

import argparse
import logging
import sys
# sudo pip install pyserial==3.4
from serial import Serial, serialutil
# sudo apt install python3-redis
import redis


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


# some class
class FrameHandler:
    """ Modbus frame processing. """

    def __init__(self):
        # public
        self.f_counter = 0

    def process_frame(self, frame: bytes):
        # update frame counter
        self.f_counter += 1
        # current or debug mode
        if not args.debug:
            rdb.publish(args.pub_key, frame)
        else:
            # check CRC
            crc_ok = crc16(frame) == 0
            crc_status = 'OK' if crc_ok else 'ERROR'
            # log frame data
            logger.debug(f'dump #{self.f_counter:<6} CRC {crc_status:5} {frame.hex(":")}')


class ModbusSerialWorker:
    """ A serial worker to manage I/O with RTU devices. """

    def __init__(self, port: Serial, handler: FrameHandler, eof_ms: float = 50.0):
        # public
        self.serial_port = port
        self.handler = handler
        self.eof_ms = eof_ms

    def loop(self):
        """ Serial worker main loop. """
        # flush rx buffer
        self.serial_port.reset_input_buffer()
        # receive loop
        while True:
            # wait for first byte of frame
            self.serial_port.timeout = None
            frame = self.serial_port.read(1)
            # if ok, wait for the remaining
            if frame:
                # wait for next bytes of data until end of frame delay
                self.serial_port.timeout = self.eof_ms / 1000
                while True:
                    f_chunk = self.serial_port.read(1)
                    if f_chunk:
                        frame += f_chunk
                        # limit size to 256 bytes
                        frame = frame[-256:]
                    else:
                        break
                # call frame handler
                self.handler.process_frame(frame)


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('device', type=str, help='serial device (like /dev/ttyUSB0)')
    parser.add_argument('pub_key', type=str, help='redis publish key (like ch1:frames)')
    parser.add_argument('-b', '--baudrate', type=int, default=9600, help='serial rate (default is 9600)')
    parser.add_argument('-p', '--parity', type=str, default='N', help='serial parity (default is "N")')
    parser.add_argument('-s', '--stop', type=float, default=1, help='serial stop bits (default is 1)')
    parser.add_argument('-e', '--eof_ms', type=float, default=6.0, help='end of frame delay (default is 6 ms)')
    parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
    args = parser.parse_args()
    # init logging
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger(__name__)
    try:
        # init redis DB
        rdb = redis.StrictRedis()
        # init serial port
        logging.info(f'start serial port monitor {args.device} at {args.baudrate} bauds (eof = {args.eof_ms:.3f} ms)')
        logging.info(f'relay modbus frames to "{args.pub_key}" redis channel')
        serial_port = Serial(port=args.device, baudrate=args.baudrate, parity=args.parity, stopbits=args.stop)
        # init serial worker
        serial_worker = ModbusSerialWorker(port=serial_port, handler=FrameHandler(), eof_ms=args.eof_ms)
        serial_worker.loop()
    except serialutil.SerialException as e:
        logger.error(f'serial device error: {e:r}')
        exit(1)
    except redis.RedisError as e:
        logging.error(f'redis error occur: {e!r}')
        exit(2)

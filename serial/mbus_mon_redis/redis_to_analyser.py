#!/usr/bin/env python3

""" Modbus frame analyzer. """

import argparse
import logging
import struct
import sys
import time
# sudo apt install python3-redis
import redis


# some consts
# functions codes
READ_COILS = 0x01
READ_DISCRETE_INPUTS = 0x02
READ_HOLDING_REGISTERS = 0x03
READ_INPUT_REGISTERS = 0x04
WRITE_SINGLE_COIL = 0x05
WRITE_SINGLE_REGISTER = 0x06
WRITE_MULTIPLE_COILS = 0x0F
WRITE_MULTIPLE_REGISTERS = 0x10
WRITE_READ_MULTIPLE_REGISTERS = 0x17
ENCAPSULATED_INTERFACE_TRANSPORT = 0x2B


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
class FrameType:
    UNKNOWN = 0
    REQUEST = 1
    RESPONSE = 2


class ModbusRTUFrame:
    """ Modbus RTU frame container class. """

    def __init__(self, raw=b'', is_request: bool = False):
        # public
        self.raw = raw
        # flags
        self.is_request = is_request

    def __bool__(self):
        return bool(self.raw)

    def __len__(self):
        return len(self.raw)

    @property
    def type_as_str(self):
        """Return request/response type as string."""
        return 'request' if self.is_request else 'response'

    @property
    def pdu(self):
        """Return PDU part of frame."""
        return self.raw[1:-2]

    @property
    def slv_addr(self):
        """Return slave address part of frame."""
        try:
            return self.raw[0]
        except IndexError:
            return

    @property
    def func_code(self):
        """Return function code part of frame."""
        try:
            return self.raw[1]
        except IndexError:
            return

    @property
    def except_code(self):
        """Return except code part of frame."""
        try:
            return self.raw[2]
        except IndexError:
            return

    @property
    def is_valid(self):
        """Check if frame is valid.

        :return: True if frame is valid
        :rtype: bool
        """
        return len(self.raw) > 4 and crc16(self.raw) == 0


class FrameAnalyzer:
    """ Modbus frame processing. """

    def __init__(self):
        # public
        self.nb_frame = 0
        self.nb_good_crc = 0
        self.nb_bad_crc = 0
        # current and last frame
        self.frm_now = ModbusRTUFrame()
        self.frm_last = ModbusRTUFrame()
        # private
        # modbus default functions map
        self._analyze_func_map = {READ_COILS: self._msg_read_bits,
                                  READ_DISCRETE_INPUTS: self._msg_read_bits,
                                  READ_HOLDING_REGISTERS: self._msg_read_words,
                                  READ_INPUT_REGISTERS: self._msg_read_words, }
        # WRITE_SINGLE_COIL: self._write_single_coil,
        # WRITE_SINGLE_REGISTER: self._write_single_register,
        # WRITE_MULTIPLE_COILS: self._write_multiple_coils,
        # WRITE_MULTIPLE_REGISTERS: self._write_multiple_registers,
        # WRITE_READ_MULTIPLE_REGISTERS: self._write_read_multiple_registers,
        # ENCAPSULATED_INTERFACE_TRANSPORT: self._encapsulated_interface_transport}

    def _msg_crc_err(self):
        return f"bad CRC (raw: {self.frm_now.raw.hex(':')})"

    def _msg_except(self):
        # except frame is always a response
        self.frm_now.is_request = False
        # format analyze message
        origin_func = self.frm_now.func_code - 0x80
        return f'reponse is an exception (code 0x{self.frm_now.except_code:02x}) ' \
               f'for function 0x{origin_func:02x} (slave 0x{self.frm_now.slv_addr:02x}'

    def _msg_func_unknown(self):
        return f'unknown function 0x{self.frm_now.func_code:02x} (slave 0x{self.frm_now.slv_addr:02x})'

    def _msg_read_bits(self):
        # request or response ?
        # 8 bytes long frame -> request or response, other length -> response
        if len(self.frm_now) == 8:
            self.frm_now.is_request = not self.frm_last.is_request
        else:
            self.frm_now.is_request = False
        # format analyze message
        f_name = 'read coils' if self.frm_now.func_code == READ_COILS else 'read discrete inputs'
        return f'{self.frm_now.type_as_str} {f_name}'

    def _msg_read_words(self):
        # request or response ?
        # 8 bytes long frame -> request, other length -> response
        self.frm_now.is_request = len(self.frm_now) == 8
        # decode frame PDU
        if self.frm_now.is_request:
            # request
            try:
                reg_addr, reg_nb = struct.unpack('>hh', self.frm_now.pdu[1:])
                msg_pdu = f'read {reg_nb} register(s) at @0x{reg_addr:04x} ({reg_addr})'
            except struct.error:
                msg_pdu = 'error during frame decoding'
        else:
            # response
            try:
                byte_nb = struct.unpack('B', self.frm_now.pdu[1:2])[0]
                msg_pdu = f'return {byte_nb} byte(s)'
            except struct.error:
                msg_pdu = 'error during frame decoding'
        # format analyze message
        f_name = 'read holding registers' if self.frm_now.func_code == READ_HOLDING_REGISTERS else 'read inputs registers'
        return f'{self.frm_now.type_as_str} "{f_name}": {msg_pdu}'

    def analyze(self, frame: bytes):
        # check CRC
        self.frm_now = ModbusRTUFrame(frame)
        crc_ok = self.frm_now.is_valid
        # debug: log raw frame
        crc_status = 'OK' if crc_ok else 'ERROR'
        logger.debug(f'dump #{self.nb_frame:<6} CRC {crc_status:5} {frame.hex(":")}')
        # update frame counter
        self.nb_frame += 1
        # msg header
        msg = f'[slave @{self.frm_now.slv_addr}] '
        # analyze only valid frame
        if crc_ok:
            self.nb_good_crc += 1
            # check exception status
            if self.frm_now.func_code >= 0x80:
                # on except
                msg += self._msg_except()
            else:
                # if no except, call the ad-hoc function, if none exists, send an "illegal function" exception
                try:
                    msg += self._analyze_func_map[self.frm_now.func_code]()
                except KeyError:
                    msg += self._msg_func_unknown()
            # keep current frame (with good CRC) for next analyze
            self.frm_last = self.frm_now
        else:
            # don't analyze frame with bad CRC
            self.nb_bad_crc += 1
            msg += self._msg_crc_err()
        # show msg
        logging.info(msg)


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('pub_key', type=str, help='redis publish key (like ch1:frames)')
    parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
    args = parser.parse_args()
    # init logging
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger(__name__)
    # init frame analyser
    frame_analyzer = FrameAnalyzer()
    # startup message
    logging.info(f'analyze modbus frames from "{args.pub_key}" redis channel')
    # redis DB loop (ensure retry on except)
    while True:
        try:
            # connect to redis DB
            rdb = redis.StrictRedis()
            # subscribe to pub_key channel
            rps = rdb.pubsub()
            rps.subscribe(args.pub_key)
            # process messages
            for item in rps.listen():
                if item.get('type') == 'message':
                    frame_analyzer.analyze(item.get('data', b''))
        except redis.RedisError as e:
            logging.error(f'redis error occur: {e!r}')
            time.sleep(1.0)
        except KeyboardInterrupt:
            exit(0)

#!/usr/bin/env python3

""" Modbus frame analyzer. """

import argparse
import logging
import os
import struct
import sys
import time
# sudo apt install python3-redis
import redis

# some consts
# function codes
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
# custom function codes
GET_ALL_HOURLY_STATION_DATA = 0x64
GET_ALL_DAILY_STATION_DATA = 0x65
GET_ALL_HOURLY_LINE_DATA = 0x66
GET_ALL_DAILY_LINE_DATA = 0x67
GET_ALL_GAS_AUX_HOURLY_STATION_DATA = 0x68
GET_DETAILED_HOURLY_STATION_DATA = 0x69


# some functions
def crc16(frame: bytes) -> int:
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
class ModbusRTUFrame:
    """ Modbus RTU frame container class. """

    def __init__(self, raw=b'', is_request: bool = False):
        # public
        self.raw = raw
        # flags
        self.is_request = is_request

    def __bool__(self) -> bool:
        return bool(self.raw)

    def __len__(self) -> int:
        return len(self.raw)

    @property
    def is_request_as_str(self) -> str:
        """Return request/response type as string."""
        return 'request' if self.is_request else 'response'

    @property
    def pdu(self) -> bytes:
        """Return PDU part of frame."""
        return self.raw[1:-2]

    @property
    def slv_addr(self) -> int or None:
        """Return slave address part of frame."""
        try:
            return self.raw[0]
        except IndexError:
            return

    @property
    def func_code(self) -> int or None:
        """Return function code part of frame."""
        try:
            return self.raw[1]
        except IndexError:
            return

    @property
    def except_code(self) -> int or None:
        """Return except code part of frame."""
        try:
            return self.raw[2]
        except IndexError:
            return

    @property
    def is_valid(self) -> bool:
        """Check if frame is valid.

        :return: True if frame is valid
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
        # modbus functions maps
        self._func_methods = {READ_COILS: self._msg_read_bits,
                              READ_DISCRETE_INPUTS: self._msg_read_bits,
                              READ_HOLDING_REGISTERS: self._msg_read_words,
                              READ_INPUT_REGISTERS: self._msg_read_words,
                              WRITE_SINGLE_COIL: self._msg_write_single_coil,
                              WRITE_SINGLE_REGISTER: self._msg_write_single_reg,
                              WRITE_MULTIPLE_COILS: self._msg_write_multiple_coils,
                              WRITE_MULTIPLE_REGISTERS: self._msg_write_multiple_registers,
                              GET_ALL_HOURLY_STATION_DATA: self._msg_get_all_hourly_data}
        self._func_names = {READ_COILS: 'read coils (1)',
                            READ_DISCRETE_INPUTS: 'read discrete inputs (2)',
                            READ_HOLDING_REGISTERS: 'read holding registers (3)',
                            READ_INPUT_REGISTERS: 'read input registers (4)',
                            WRITE_SINGLE_COIL: 'write single coil (5)',
                            WRITE_SINGLE_REGISTER: 'write single register (6)',
                            WRITE_MULTIPLE_COILS: 'write multiple coils (15)',
                            WRITE_MULTIPLE_REGISTERS: 'write multiple registers (16)',
                            WRITE_READ_MULTIPLE_REGISTERS: 'write read multiple registers (23)',
                            ENCAPSULATED_INTERFACE_TRANSPORT: 'encapsulated interface transport (43)',
                            GET_ALL_HOURLY_STATION_DATA: 'get all hourly station data (100)',
                            GET_ALL_DAILY_STATION_DATA: 'get all daily station data (101)',
                            GET_ALL_HOURLY_LINE_DATA: 'get all hourly line data (102)',
                            GET_ALL_DAILY_LINE_DATA: 'get all daily line data (103)',
                            GET_ALL_GAS_AUX_HOURLY_STATION_DATA: 'get all gas auxiliary hourly station data (104)',
                            GET_DETAILED_HOURLY_STATION_DATA: 'get detailed hourly station data (105)'}

    def _msg_crc_err(self) -> str:
        return f"bad CRC (raw: {self.frm_now.raw.hex(':')})"

    def _msg_except(self) -> str:
        # override request or response flag
        # except frame is always a response
        self.frm_now.is_request = False
        # format analyze message
        return f'response: exception (code 0x{self.frm_now.except_code:02x})'

    def _msg_func_unknown(self) -> str:
        # format message
        return (f'{self.frm_now.is_request_as_str} function not supported: '
                f'"{self.func_name_by_id(self.frm_now.func_code)}"')

    def _msg_read_bits(self) -> str:
        # override request or response flag
        # 8 bytes long frame -> request or response, other length -> always a response
        if len(self.frm_now) != 8:
            self.frm_now.is_request = False
        # decode frame PDU
        if self.frm_now.is_request:
            # request
            try:
                bit_addr, bit_nb = struct.unpack('>HH', self.frm_now.pdu[1:])
                msg_pdu = f'read {bit_nb} bit(s) at @ 0x{bit_addr:04x} ({bit_addr})'
            except struct.error:
                msg_pdu = 'bad PDU format'
        else:
            # response
            try:
                read_bytes, = struct.unpack('>B', self.frm_now.pdu[1:2])
                bytes_l = struct.unpack(f'>{read_bytes}B', self.frm_now.pdu[2:])
                # format bytes_l as bits list str: "1, 0, 1, 0 ..."
                bits_l = []
                for byte_val in bytes_l:
                    for n in range(8):
                        bits_l.append('1' if (byte_val & (1 << n)) else '0')
                bits_str = ', '.join(bits_l)
                msg_pdu = f'return {len(bits_l)} bit(s) (read bytes={read_bytes}) data: [{bits_str}]'
            except struct.error:
                msg_pdu = 'bad PDU format'
        # format message
        return f'{self.frm_now.is_request_as_str}: {msg_pdu}'

    def _msg_read_words(self) -> str:
        # override request or response flag
        # 8 bytes long frame -> request, other length -> response
        self.frm_now.is_request = len(self.frm_now) == 8
        # decode frame PDU
        if self.frm_now.is_request:
            # request
            try:
                reg_addr, regs_nb = struct.unpack('>HH', self.frm_now.pdu[1:])
                msg_pdu = f'read {regs_nb} register(s) at @ 0x{reg_addr:04x} ({reg_addr})'
            except struct.error:
                msg_pdu = 'bad PDU format'
        else:
            # response
            try:
                read_bytes, = struct.unpack('>B', self.frm_now.pdu[1:2])
                regs_l = struct.unpack(f'>{read_bytes // 2}H', self.frm_now.pdu[2:])
                regs_str = ', '.join([f'{r:d}' for r in regs_l])
                msg_pdu = f'return {len(regs_l)} register(s) (read bytes={read_bytes}) data: [{regs_str}]'
            except struct.error:
                msg_pdu = 'bad PDU format'
        # format message
        return f'{self.frm_now.is_request_as_str}: {msg_pdu}'

    def _msg_write_single_coil(self) -> str:
        # request and response
        try:
            bit_addr, bit_value, _ = struct.unpack('>HBB', self.frm_now.pdu[1:])
            bit_value_str = '1' if bit_value == 0xFF else '0'
            msg_pdu = f'write {bit_value_str} to coil at @ 0x{bit_addr:04x} ({bit_addr})'
            if not self.frm_now.is_request:
                msg_pdu += ' OK'
        except struct.error:
            msg_pdu = 'bad PDU format'
        # format message
        return f'{self.frm_now.is_request_as_str}: {msg_pdu}'

    def _msg_write_single_reg(self) -> str:
        # request and response
        try:
            reg_addr, reg_value = struct.unpack('>HH', self.frm_now.pdu[1:])
            msg_pdu = f'write {reg_value} to register at @ 0x{reg_addr:04x} ({reg_addr})'
            if not self.frm_now.is_request:
                msg_pdu += ' OK'
        except struct.error:
            msg_pdu = 'bad PDU format'
        # format message
        return f'{self.frm_now.is_request_as_str}: {msg_pdu}'

    def _msg_write_multiple_coils(self) -> str:
        # override request or response flag
        # 8 bytes long frame -> response, other length -> request
        self.frm_now.is_request = len(self.frm_now) != 8
        # decode frame PDU
        if self.frm_now.is_request:
            # request
            try:
                bit_addr, bits_nb, bytes_nb = struct.unpack('>HHb', self.frm_now.pdu[1:6])
                bytes_l = struct.unpack(f'>{bytes_nb}B', self.frm_now.pdu[6:])
                # format bytes_l as bits list str: "1, 0, 1, 0 ..."
                bits_l = []
                for byte_val in bytes_l:
                    for n in range(8):
                        bits_l.append('1' if (byte_val & (1 << n)) else '0')
                bits_str = ', '.join(bits_l)
                msg_pdu = f'write {bits_nb} bit(s) at @ 0x{bit_addr:04x} ({bit_addr}) data: [{bits_str}]'
            except struct.error:
                msg_pdu = 'bad PDU format'
        else:
            # response
            try:
                bit_addr, bits_nb = struct.unpack('>HH', self.frm_now.pdu[1:5])
                msg_pdu = f'write {bits_nb} bit(s) at @ 0x{bit_addr:04x} ({bit_addr}) OK'
            except struct.error:
                msg_pdu = 'bad PDU format'
        # format message
        return f'{self.frm_now.is_request_as_str}: {msg_pdu}'

    def _msg_write_multiple_registers(self) -> str:
        # override request or response flag
        # 8 bytes long frame -> response, other length -> request
        self.frm_now.is_request = len(self.frm_now) != 8
        # decode frame PDU
        if self.frm_now.is_request:
            # request
            try:
                reg_addr, regs_nb, bytes_nb = struct.unpack('>HHb', self.frm_now.pdu[1:6])
                regs_l = struct.unpack(f'>{bytes_nb//2}H', self.frm_now.pdu[6:])
                regs_str = ', '.join([str(b) for b in regs_l])
                msg_pdu = f'write {regs_nb} register(s) at @ 0x{reg_addr:04x} ({reg_addr}) data: [{regs_str}]'
            except struct.error:
                msg_pdu = f'bad PDU format'
        else:
            # response
            try:
                reg_addr, regs_nb = struct.unpack('>HH', self.frm_now.pdu[1:5])
                msg_pdu = f'write {regs_nb} register(s) at @ 0x{reg_addr:04x} ({reg_addr}) OK'
            except struct.error:
                msg_pdu = 'bad PDU format'
        # format message
        return f'{self.frm_now.is_request_as_str}: {msg_pdu}'

    def _msg_get_all_hourly_data(self) -> str:
        # override request or response flag
        # 8 bytes long frame -> request, other length -> response
        self.frm_now.is_request = len(self.frm_now) == 8
        # decode frame PDU
        if self.frm_now.is_request:
            # request
            try:
                hour_id, byte_qty = struct.unpack('>Ib', self.frm_now.pdu[1:6])
                msg_pdu = f'read hourly data hour ID={hour_id} and byte qty={byte_qty}'
            except struct.error:
                msg_pdu = f'bad PDU format'
        else:
            # response
            try:
                msg_pdu = 'implement this'
                #reg_addr, regs_nb = struct.unpack('>HH', self.frm_now.pdu[1:5])
                #msg_pdu = f'write {regs_nb} register(s) at @ 0x{reg_addr:04x} ({reg_addr}) OK'
            except struct.error:
                msg_pdu = 'bad PDU format'
        # format message
        return f'{self.frm_now.is_request_as_str}: {msg_pdu}'

    def func_name_by_id(self, func_id: int) -> str:
        """ Translate function code to name or hex representation. """
        if func_id >= 0x80:
            func_id -= 0x80
        return self._func_names.get(func_id, f'0x{func_id:02x}')

    def analyze(self, frame: bytes):
        """ Process current frame and produce a message to stdout. """
        # check CRC
        self.frm_now = ModbusRTUFrame(frame)
        # update frame counter
        self.nb_frame += 1
        # debug: log raw frame
        logger.debug(f'[{self.nb_frame:>6}] frame dump: {frame.hex(":")}')
        # msg header
        f_name = self.func_name_by_id(self.frm_now.func_code)
        msg = f'[{self.nb_frame:>6}] slave {self.frm_now.slv_addr} "{f_name}" '
        # analyze only valid frame
        if self.frm_now.is_valid:
            self.nb_good_crc += 1
            # fix default request/response flag (can be override in _msg_xxxx func methods)
            slv_addr_chg = self.frm_now.slv_addr != self.frm_last.slv_addr
            func_code_chg = self.frm_now.func_code != self.frm_last.func_code
            self.frm_now.is_request = True if slv_addr_chg or func_code_chg else not self.frm_last.is_request
            # check exception status
            if self.frm_now.func_code >= 0x80:
                # on except
                msg += self._msg_except()
            else:
                # if no except, call the ad-hoc function, if none exists, send an "illegal function" exception
                try:
                    msg += self._func_methods[self.frm_now.func_code]()
                except KeyError:
                    msg += self._msg_func_unknown()
            # keep current frame (with good CRC) for next analyze
            self.frm_last = self.frm_now
        else:
            # don't analyze frame with bad CRC
            self.nb_bad_crc += 1
            msg += self._msg_crc_err()
        # show message
        logger.info(msg)


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
    # when stdout is piped to another process
    if not sys.stdout.isatty():
        # avoid "BrokenPipeError" catch by logging internal handleError
        logging.raiseExceptions = False
    logger = logging.getLogger(__name__)
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # init frame analyser
    frame_analyzer = FrameAnalyzer()
    # startup message
    logger.debug(f'analyze modbus frames from "{args.pub_key}" redis channel')
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
                    # ensure "BrokenPipeError" is trig in this code block
                    sys.stdout.flush()
        except BrokenPipeError:
            # avoid "BrokenPipeError" when connect stdout to a died process
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
            exit(1)
        except redis.RedisError as e:
            logger.error(f'redis error occur: {e!r}')
            time.sleep(1.0)
        except KeyboardInterrupt:
            exit(0)

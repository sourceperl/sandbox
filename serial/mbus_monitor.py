#!/usr/bin/env python3

from datetime import datetime
import time
import serial


# some const
SERIAL_PORT = '/dev/ttySC0'
BAUDRATE = 115_200


# some functions
def crc16(data: bytearray):
    crc = 0xFFFF
    for byte in bytearray(data):
        next_byte = byte
        crc ^= next_byte
        for i in range(8):
            lsb = crc & 1
            crc >>= 1
            if lsb:
                crc ^= 0xA001
    return crc


def frame2hex(frame: bytearray):
    return '-'.join([f'{b:02X}' for b in frame])


def check_crc_ok(frame: bytearray):
    try:
        assert len(frame) > 2
        cp_crc = crc16(frame[:-2])
        rx_crc = int.from_bytes(frame[-2:], 'little')
        return cp_crc == rx_crc
    except:
        return False


if __name__ == '__main__':
    # init serial port
    s = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE)

    # some vars
    t_eof = 18 * 3.5 * 1/(BAUDRATE/10)
    crc_ok_count = 0
    crc_ko_count = 0
    frame_nb = 0
    t_last_rx = None
    b_rx_buf = bytearray()

    # flush buffer
    s.read_all()

    # receive loop
    while True:
        # if rx data available on serial port
        if s.in_waiting:
            # read all data and s
            t_last_rx = time.monotonic()
            b_rx_buf.extend(s.read_all())
            # limit rx buffer size
            b_rx_buf = b_rx_buf[:512]
        # if last receive time is define and rx buffer is not empty
        if t_last_rx is not None and len(b_rx_buf) > 0:
            # test if end of frame occur
            if (time.monotonic() - t_last_rx) > t_eof:
                # skip first frame (probably partial)
                if frame_nb > 0:
                    # frame CRC check
                    if check_crc_ok(b_rx_buf):
                        crc_status = 'OK'
                        crc_ok_count += 1
                    else:
                        crc_status = 'ERR'
                        crc_ko_count += 1
                    # dump frame
                    hex_frame = frame2hex(b_rx_buf)[:80]
                    date_str = datetime.now().isoformat(sep=' ', timespec='milliseconds')
                    print(f'{date_str} [#{frame_nb:>6}] [{len(b_rx_buf):>3}] [{crc_status:<3}] [{crc_ok_count:>5}|{crc_ko_count:>5}] [eof {t_eof:0.4f}]: {hex_frame}')
                # frame index
                frame_nb += 1
                # clear the rx buffer
                b_rx_buf.clear()
        # avoid high CPU consumption
        time.sleep(0.001)

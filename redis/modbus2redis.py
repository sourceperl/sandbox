#!/usr/bin/env python3

"""Pull some modbus data and publish it on redis keys."""

import time
import logging
# sudo pip3 install pyModbusTCP==0.2.0
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import decode_ieee, word_list_to_long
# sudo apt install python3-redis
import redis
# sudo apt install python3-schedule
import schedule


# define schedule jobs
def modbus_job():
    """Periodic modbus refresh job."""
    try:
        # do modbus requests on slave @3
        mcl.unit_id = 3
        # bool read
        coils_l = mcl.read_coils(20488, 1)
        logging.debug(f'read 1 coil at @20488 return {coils_l}')
        # float read
        regs_l = mcl.read_holding_registers(514, 2)
        logging.debug(f'read 2 registers at @514 return {regs_l}')
        # process requests results
        if coils_l:
            rdb.set('cvm16:good', int(coils_l[0]), ex=120)
        if regs_l:
            # convert to IEEE 754 float
            floats_l = [decode_ieee(f) for f in word_list_to_long(regs_l)]
            rdb.set('cvm16:wobbe', round(floats_l[0], 2), ex=120)
    except redis.RedisError as e:
        logging.error(f'redis error occur: {e!r}')


if __name__ == '__main__':
    # logging setup
    logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(message)s', level=logging.INFO)
    logging.getLogger('schedule').setLevel(logging.WARNING)
    # log startup
    logging.info('import-modbus-app started')

    # init redis DB
    rdb = redis.StrictRedis()
    # init modbus client (connect to serial gateway)
    mcl = ModbusClient(host='localhost', port=5020)
    # set schedule config
    schedule.every(2).seconds.do(modbus_job)

    # first call
    modbus_job()

    # main loop
    while True:
        schedule.run_pending()
        time.sleep(1.0)

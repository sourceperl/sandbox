#!/usr/bin/env python3

"""Push some feeds from redis keys to adafruit IO server."""

import time
import logging
import urllib.error
from urllib.request import urlopen, Request
from private_data import AIO_USER, AIO_KEY
# sudo apt install python3-redis
import redis
# sudo apt install python3-schedule
import schedule


# define schedule jobs
def aio_job():
    """Periodic adafruit IO update job."""
    try:
        # init feeds dict
        feeds_d = dict()
        # populate it with valid redis values
        # feed cvm16_good
        try:
            r_value = int(rdb.get('cvm16:good'))
            if r_value not in [0, 1]:
                raise ValueError
            feeds_d['cvm16-good'] = r_value
        except (TypeError, ValueError):
            logging.warning(f'unable to process redis key "cvm16:good" value must be 0 or 1')
        # feed cvm16_wobbe
        try:
            feeds_d['cvm16-wobbe'] = round(float(rdb.get('cvm16:wobbe')), 2)
        except (TypeError, ValueError):
            logging.warning(f'unable to process redis key "cvm16:wobbe" value must be a valid float')
        # update aio
        for feed_key, value in feeds_d.items():
            try:
                # build request
                req = Request(f'https://io.adafruit.com/api/v2/{AIO_USER}/feeds/{feed_key}/data')
                req.add_header('X-AIO-Key', AIO_KEY)
                req.data = f'value={value}'.encode()
                # do request
                resp = urlopen(req, timeout=5.0)
                # request status
                if resp.status == 200:
                    js_str = resp.read().decode()
                    logging.info(f'data write ok (json data: {js_str})')
                else:
                    logging.warning(f'unable to write data')
            except urllib.error.URLError as e:
                print(f'urllib error occur: {e!r}')
    except redis.RedisError as e:
        logging.error(f'redis error occur: {e!r}')


if __name__ == '__main__':
    # logging setup
    logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(message)s', level=logging.INFO)
    logging.getLogger('schedule').setLevel(logging.WARNING)
    # log startup
    logging.info('aio-sender-app started')

    # init redis DB
    rdb = redis.StrictRedis()

    # schedule config
    schedule.every(2).minutes.do(aio_job)

    # first call
    aio_job()

    # main loop
    while True:
        schedule.run_pending()
        time.sleep(1.0)

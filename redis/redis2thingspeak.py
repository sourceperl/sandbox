#!/usr/bin/env python3

"""Push some data from redis keys to thingspeak server."""

import time
import logging
import urllib.error
from urllib.parse import urlencode
from urllib.request import urlopen
from private_data import API_KEY
# sudo apt install python3-redis
import redis
# sudo apt install python3-schedule
import schedule


# define schedule jobs
def thingspeak_job():
    """Periodic thingspeak update job."""
    try:
        # init thingspeak data dict
        data_d = dict()
        # populate it with valid redis values
        try:
            r_value = int(rdb.get('cvm16:good'))
            if r_value not in [0, 1]:
                raise ValueError
            data_d['field1'] = r_value
        except (TypeError, ValueError):
            logging.warning(f'unable to process redis key "cvm16:good" value must be 0 or 1')
        try:
            data_d['field2'] = round(float(rdb.get('cvm16:wobbe')), 2)
        except (TypeError, ValueError):
            logging.warning(f'unable to process redis key "cvm16:wobbe" value must be a valid float')
        # add API key
        data_d['api_key'] = API_KEY
        # do thingspeak request
        resp = urlopen(f'https://api.thingspeak.com/update?{urlencode(data_d)}', timeout=5.0)
        # print request status
        try:
            # HTTP request return current entry ID or 0 on error
            entry_id = int(resp.read())
            if entry_id < 1:
                raise ValueError
            logging.info(f'successful data update to entry ID: {entry_id}')
        except ValueError:
            logging.warning(f'unable to update data')
    except redis.RedisError as e:
        logging.error(f'redis error occur: {e!r}')
    except urllib.error.URLError as e:
        logging.error(f'network error occur: {e!r}')


if __name__ == '__main__':
    # logging setup
    logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(message)s', level=logging.INFO)
    logging.getLogger('schedule').setLevel(logging.WARNING)
    # log startup
    logging.info('export-thingspeak-app started')

    # init redis DB
    rdb = redis.StrictRedis()

    # schedule config
    schedule.every(2).minutes.do(thingspeak_job)

    # first call
    thingspeak_job()

    # main loop
    while True:
        schedule.run_pending()
        time.sleep(1.0)

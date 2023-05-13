#!/usr/bin/env python3

from datetime import datetime
import time
import io
import sys
import urllib.request
# sudo pip3 install schedule
import schedule
# sudo apt install python3-pil python3-pil.imagetk
import PIL.Image
# sudo apt install python3-redis
import redis


# some const
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_KEY = 'webcam_img'
IMG_URL = 'https://www.infoclimat.fr/cartes/getProxyWebcam.php?idw=471&c=30&t=jpg&26318'


# some function
def webcam_polling_job():
    # log update
    print('%s: update now' % datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    # do web request
    try:
        with urllib.request.urlopen(IMG_URL, timeout=10) as u:
            raw_data = u.read()
        # convert RAW img format (bytes) to Pillow image
        pil_img = PIL.Image.open(io.BytesIO(raw_data))
        # resize to 1280x720 (720p) and force jpeg format
        pil_img.thumbnail([1280, 720])
        io_to_redis = io.BytesIO()
        pil_img.save(io_to_redis, format='JPEG')
        # send jpeg data to redis
        rc.set(REDIS_KEY, io_to_redis.getvalue())
    except Exception as err:
        print(err, file=sys.stderr)


# init redis client
rc = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
# init scheduler
schedule.every().minutes.at(':30').do(webcam_polling_job)
webcam_polling_job()

# main loop
while True:
    schedule.run_pending()
    time.sleep(1)

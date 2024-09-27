#!/usr/bin/env python3

import io
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import PIL.Image
import schedule

# some const
IMG_URL = 'http://192.168.0.200/record/current.jpg'


# some function
def webcam_job():
    # do web request
    try:
        # get image from webcam
        with urllib.request.urlopen(IMG_URL, timeout=4.0) as u:
            raw_data = u.read()
        # convert RAW img format (bytes) to Pillow image
        pil_img = PIL.Image.open(io.BytesIO(raw_data))
        # crop to square image
        pil_img = pil_img.crop((160, 0, 640, 480))
        # resize to 244x244
        pil_img.thumbnail((244, 244))
        # save current sample in directory
        img_name = f"{datetime.now(timezone.utc).astimezone().isoformat()}.jpg"
        pil_img.save(Path('samples') / img_name, format='JPEG')
    except Exception as e:
        print(e, file=sys.stderr)


# init scheduler
schedule.every(10).seconds.do(webcam_job)
webcam_job()

# main loop
while True:
    schedule.run_pending()
    time.sleep(1)

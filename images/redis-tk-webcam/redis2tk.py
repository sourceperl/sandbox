#!/usr/bin/env python3

from datetime import datetime
import io
import sys
import tkinter as tk
# sudo apt install python3-pil python3-pil.imagetk
import PIL.Image
import PIL.ImageTk
# sudo apt install python3-redis
import redis


# some const
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_KEY = 'webcam_img'


# build tk interface
class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # init redis client
        self.rc = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        # img container
        self.lbl_img = tk.Label()
        self.lbl_img.pack()
        # start auto-refresh
        self.update_img()

    def update_img(self):
        # log update
        print('%s: update now' % datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        # update tk image label
        try:
            # redis request
            raw_data = self.rc.get(REDIS_KEY)
            # RAW img data to Pillow (PIL) image
            pil_img = PIL.Image.open(io.BytesIO(raw_data))
            # force size to 1280x720
            pil_img.thumbnail([1280, 720])
            # convert PIL image to Tk format
            tk_img = PIL.ImageTk.PhotoImage(pil_img)
            self.lbl_img.configure(image=tk_img)
            # don't remove: keep a ref to avoid del by garbage collect
            self.lbl_img.tk_img = tk_img
        except Exception as err:
            print(err, file=sys.stderr)
        # redo after 2s
        self.after(2000, func=self.update_img)


if __name__ == '__main__':
    app = MainApp()
    app.title('Webcam test from redis DB')
    app.mainloop()

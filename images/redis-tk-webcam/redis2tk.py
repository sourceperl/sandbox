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
        # add canvas
        self.cvs = tk.Canvas(width=1280, height=720, bd=0)
        self.cvs.pack()
        # add mouse left click handler to canvas
        self.cvs.bind('<Button-1>', self._cvs_left_click)
        # add image to canvas
        self.cvs_img = self.cvs.create_image(0, 0, anchor=tk.NW)
        # mark an area on canvas
        self.cvs.create_rectangle(70, 142, 230, 274, outline='red')
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
            # convert PIL image to Tk format and load it
            tk_img = PIL.ImageTk.PhotoImage(pil_img)
            self.cvs.itemconfig(self.cvs_img, image=tk_img)
            # don't remove: keep a ref to avoid garbage collect deletion
            self.cvs.tk_img = tk_img
        except Exception as err:
            print(err, file=sys.stderr)
        # redo after 2s
        self.after(2000, func=self.update_img)
    
    def _cvs_left_click(self, event):
        print(f'Canvas coordinates: x={event.x}, y={event.y}')


if __name__ == '__main__':
    app = MainApp()
    app.title('Webcam test from redis DB')
    app.mainloop()

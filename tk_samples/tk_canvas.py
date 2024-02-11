#!/usr/bin/env python3

""" 
A Tk canvas example.

"""

from math import cos, sin
import time
from typing import List
import tkinter as tk


# some class
class MyCanvas(tk.Canvas):
    def create_disk(self, x: float, y: float, size: float = 20.0, **kwargs) -> int:
        h_size = size/2
        return self.create_oval(x-h_size, y-h_size, x+h_size, y+h_size, **kwargs)

    def xy_coords(self, __tagOrId: str | int) -> List[float]:
        x0, y0, x1, y1 = self.coords(__tagOrId)
        return x0+(x1-x0)/2, y0+(y1-y0)/2

    def set_xy_coords(self, __tagOrId: str | int, x: float, y: float) -> None:
        x0, y0, x1, y1 = self.coords(__tagOrId)
        self.coords(__tagOrId, x-(x1-x0)/2, y-(y1-y0)/2, x+(x1-x0)/2, y+(y1-y0)/2)


class MainFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        # canvas setup
        self.my_can = MyCanvas(self, width=800, height=600, background='black')
        self.my_can.grid(row=0, column=0, padx=10, pady=10)
        # draw on canvas
        self.sun_disk = self.my_can.create_disk(x=400, y=300, size=40, fill='yellow')
        self.mercury_disk = self.my_can.create_disk(x=0, y=0, size=10, fill='#8c8c94')
        self.venus_disk = self.my_can.create_disk(x=0, y=0, size=10, fill='#f8e2b0')
        self.earth_disk = self.my_can.create_disk(x=0, y=0, size=20, fill='#4f4cb0')
        self.moon_disk = self.my_can.create_disk(x=0, y=0, size=5, fill='#ada8a5')
        self.mars_disk = self.my_can.create_disk(x=0, y=0, size=15, fill='#c1440e')
        self.jupiter_disk = self.my_can.create_disk(x=0, y=0, size=30, fill='#c99039')
        self.saturn_disk = self.my_can.create_disk(x=0, y=0, size=30, fill='#eddbad')
        # periodic job
        self.do_every(self.every_10ms_job, every_ms=10)

    def every_10ms_job(self):
        # now
        t0 = time.time()
        # get coordinates
        x_sun, y_sun = self.my_can.xy_coords(self.sun_disk)
        x_earth, y_earth = self.my_can.xy_coords(self.earth_disk)
        # animate mercury
        self.my_can.set_xy_coords(self.mercury_disk,
                                  x=x_sun + 40 * cos(t0*4),
                                  y=y_sun + 40 * sin(t0*4))
        # animate venus
        self.my_can.set_xy_coords(self.venus_disk,
                                  x=x_sun + 70 * cos(t0*2),
                                  y=y_sun + 70 * sin(t0*2))
        # animate earth
        self.my_can.set_xy_coords(self.earth_disk,
                                  x=x_sun + 120 * cos(t0),
                                  y=y_sun + 120 * sin(t0))
        # animate moon
        self.my_can.set_xy_coords(self.moon_disk,
                                  x=x_earth + 30 * cos(t0*6),
                                  y=y_earth + 30 * sin(t0*6))
        # animate mars
        self.my_can.set_xy_coords(self.mars_disk,
                                  x=x_sun + 180 * cos(t0/4), 
                                  y=y_sun + 180 * sin(t0/4))
        # animate jupiter
        self.my_can.set_xy_coords(self.jupiter_disk,
                                  x=x_sun + 230 * cos(t0/6),
                                  y=y_sun + 230 * sin(t0/6))
        # animate saturn
        self.my_can.set_xy_coords(self.saturn_disk,
                                  x=x_sun + 280 * cos(t0/8),
                                  y=y_sun + 280 * sin(t0/8))

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


if __name__ == '__main__':
    app = tk.Tk()
    app.wm_title('A Tk Canvas example')
    MainFrame(app).pack()
    app.mainloop()

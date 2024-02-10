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
        self.my_can = MyCanvas(self, width=600, height=400, background='black')
        self.my_can.grid(row=0, column=0, padx=10, pady=10)
        # draw on canvas
        self.sun_oval = self.my_can.create_disk(x=300, y=200, size=30, fill='yellow')
        self.mars_oval = self.my_can.create_disk(x=150, y=100, size=15, fill='orange')
        self.earth_oval = self.my_can.create_disk(x=150, y=100, size=20, fill='blue')
        self.moon_oval = self.my_can.create_disk(x=150, y=100, size=10, fill='gray')
        # periodic job
        self.do_every(self.every_10ms_job, every_ms=10)

    def every_10ms_job(self):
        # now
        t0 = time.time()
        # animate mars
        x_sun, y_sun = self.my_can.xy_coords(self.sun_oval)
        self.my_can.set_xy_coords(self.mars_oval,
                                  x=x_sun + 180 * cos(t0/4),
                                  y=y_sun + 180 * sin(t0/4))
        # animate earth
        x_sun, y_sun = self.my_can.xy_coords(self.sun_oval)
        self.my_can.set_xy_coords(self.earth_oval,
                                  x=x_sun + 120 * cos(t0/2),
                                  y=y_sun + 120 * sin(t0/2))
        # animate moon
        x_earth, y_earth = self.my_can.xy_coords(self.earth_oval)
        self.my_can.set_xy_coords(self.moon_oval,
                                  x=x_earth + 30 * cos(t0*6),
                                  y=y_earth + 30 * sin(t0*6))

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


if __name__ == '__main__':
    app = tk.Tk()
    app.wm_title('A Tk Canvas example')
    MainFrame(app).pack()
    app.mainloop()

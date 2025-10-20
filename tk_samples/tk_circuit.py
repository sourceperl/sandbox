#!/usr/bin/env python3

import tkinter as tk

import numpy as np
from scipy.interpolate import BSpline, splprep


class AccurateCircuitTrain:
    """
    A class to create a smooth, curved path circuit and animate 
    a train moving accurately along the B-spline curve using SciPy.
    """

    def __init__(self, master: tk.Frame):
        self.master = master

        # canvas setup
        self.canvas_width = 700
        self.canvas_height = 500
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="#eed799")
        self.canvas.pack()

        # main path definition
        self.path_x = [100, 250, 500, 650, 500, 250, 100, 50, 100]
        self.path_y = [100, 150, 100, 250, 400, 450, 350, 250, 100]

        # Calculate the B-spline representation (tck)
        # s=0 (interpolation), k=3 (cubic), per=True (periodic/closed)
        tck, _ = splprep([self.path_x, self.path_y], s=0, k=3, per=1)
        t, c_list, k = tck
        c_x, c_y = c_list
        self.spline_x = BSpline(t, c_x, k)
        self.spline_y = BSpline(t, c_y, k)

        # animation params
        self.anim_every_ms = 100
        self.anim_step = 0.002
        self.anim_u = 0.0

        # train params
        self.train_size = 15
        self.train_id = None

        # draw the circuit and the train
        self._draw_circuit()
        self._draw_train()

        # stop button
        tk.Button(self.master, text='Quit', command=self.master.quit).pack(pady=5)

        # start animation
        self._do_every(self.animate_train, every_ms=self.anim_every_ms)

    def _do_every(self, do_cmd, every_ms: int = 1000):
        do_cmd()
        self.master.after(every_ms, lambda: self._do_every(do_cmd, every_ms=every_ms))

    def _draw_circuit(self):
        """Draws the smooth, curved path circuit based on the spline."""

        # use the spline data to generate many points for drawing the path
        u_list = np.linspace(0.0, 1.0, 200)

        # draw the path
        x_out, y_out = self.spline_x(u_list), self.spline_y(u_list)
        path_points_list = np.transpose([x_out, y_out]).flatten().tolist()
        self.canvas.create_line(path_points_list, fill='black', width=4, smooth=False, tags='track')

        # draw the control points for reference
        for x, y in zip(self.path_x, self.path_y):
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='red', tags='control_point')

    def _draw_train(self):
        """Creates the initial train object at the start of the path."""
        # startup place
        start_x = float(self.spline_x(0.0))
        start_y = float(self.spline_y(0.0))

        # train is a small blue rectangle
        self.train_id = self.canvas.create_rectangle(
            start_x - self.train_size, start_y - self.train_size,
            start_x + self.train_size, start_y + self.train_size,
            fill='blue', outline='darkblue', tags='train'
        )
        # add a detail (headlight)
        self.canvas.create_oval(start_x - 5, start_y - 5, start_x + 5, start_y + 5, fill='yellow', tags='train')
        #self.canvas.tag_raise('train', self.train_id)

    def animate_train(self):
        """
        Main animation loop that updates the train's position.
        """
        # ensure train is draw
        if self.train_id is None:
            return

        # increment the path parameter
        self.anim_u += self.anim_step

        # loop the path
        if self.anim_u >= 1.0:
            self.anim_u = 0.0

        # get the new, highly accurate position (x, y)
        new_x, new_y = self.spline_x(self.anim_u), self.spline_y(self.anim_u)

        # get current position of the train center
        coords = self.canvas.coords(self.train_id)
        if not coords:
            return
        center_x = (coords[0] + coords[2]) / 2
        center_y = (coords[1] + coords[3]) / 2

        # calculate displacement
        dx = new_x - center_x
        dy = new_y - center_y

        # move train
        self.canvas.move('train', dx, dy)


if __name__ == '__main__':
    app = tk.Tk()
    app.title('Accurate B-Spline path animation')
    main_frame = tk.Frame(app)
    AccurateCircuitTrain(main_frame)
    main_frame.pack()
    app.mainloop()

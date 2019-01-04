#!/usr/bin/env python3

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib import style
from random import randint


# some class
class GraphFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # init data
        self.y1 = []
        self.y2 = []
        # init matplotlib graph
        style.use("ggplot")
        self.fig = Figure(figsize=(8, 5), dpi=112)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212, sharex=self.ax1)
        self.ax1.set_ylim(0, 100, auto=False)
        self.ax2.set_ylim(0, 100, auto=False)
        self.ax1.set_ylabel("y1", color="g")
        self.ax2.set_ylabel("y2", color="r")
        self.fig.set_tight_layout(True)
        # add animate graph widget to tk app
        graph = FigureCanvasTkAgg(self.fig, master=self)
        canvas = graph.get_tk_widget()
        canvas.grid(row=0, column=0)
        self.ani = animation.FuncAnimation(self.fig, self.update_graph, interval=1000)
        # update data every 1s
        self.do_every(self.update_data, every_ms=1000)

    def update_graph(self, _):
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_ylim(0, 100, auto=False)
        self.ax2.set_ylim(0, 100, auto=False)
        self.ax1.set_ylabel("y1", color="g")
        self.ax2.set_ylabel("y2", color="r")
        self.ax1.plot(self.y1, "g-o")
        self.ax2.plot(self.y2, "r-o")

    def update_data(self):
        self.y1.append(randint(0, 100))
        while len(self.y1) > 50:
            self.y1.pop(0)
        self.y2.append(randint(0, 100))
        while len(self.y2) > 50:
            self.y2.pop(0)

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))

if __name__ == "__main__":
    # main tk app loop
    app = tk.Tk()
    app.wm_title("Tk Matplotlib animation sample")
    GraphFrame(app).pack(side="top", fill="both", expand=True)
    tk.Button(app, text="Quit", command=lambda: app.destroy()).pack()
    app.mainloop()

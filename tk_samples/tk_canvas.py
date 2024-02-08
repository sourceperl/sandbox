#!/usr/bin/env python3

""" 
A Tk canvas example.
"""

import tkinter as tk


# some class
class MainFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        # canvas setup
        self.my_can = tk.Canvas(self, width=600, height=400, background='black')
        self.my_can.grid(row=0, column=0, padx=10, pady=10)
        # draw on canvas
        self.my_can.create_rectangle(10, 10, 50, 50, fill='orange')
        self.my_can.create_line((100, 100), (200, 200), width=5, fill='red')
        # periodic job
        self.do_every(self.every_1s_job, every_ms=1000)

    def every_1s_job(self):
        pass

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


if __name__ == '__main__':
    app = tk.Tk()
    app.wm_title('Tk Canvas')
    MainFrame(app).pack()
    app.mainloop()

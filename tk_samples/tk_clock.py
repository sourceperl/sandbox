#!/usr/bin/env python3

""" 
A numeric Tk clock. 
"""

from datetime import datetime
import tkinter as tk


# some class
class MainFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        # tk strings vars
        self._date_str = tk.StringVar(value='')
        self._time_str = tk.StringVar(value='')
        # widgets setup
        self.date_lbl = tk.Label(self, font=('Verdana', 64), textvariable=self._date_str)
        self.date_lbl.grid(row=0, column=0, padx=10)
        self.time_lbl = tk.Label(self, font=('Verdana', 64), textvariable=self._time_str)
        self.time_lbl.grid(row=1, column=0, padx=10)
        # periodic job
        self.do_every(self.every_1s_job, every_ms=1000)

    def every_1s_job(self):
        now_dt = datetime.now()
        self._date_str.set(now_dt.strftime('%d/%m/%Y'))
        self._time_str.set(now_dt.strftime('%H:%M:%S'))

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))


if __name__ == '__main__':
    app = tk.Tk()
    app.wm_title('Tk Clock')
    app.attributes('-fullscreen', True)
    MainFrame(app).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    app.mainloop()

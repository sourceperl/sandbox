#!/usr/bin/python3

import csv
from datetime import datetime
from os import chdir
from os.path import abspath, dirname
import time
import threading
from typing import Any
from lib.modbus import FloatModbusClient
from lib.flow_coefficient import valve_flow
import numpy as np
import tkinter as tk


# some class
class ExcelFr(csv.excel):
    delimiter = ';'


class DataItem:
    def __init__(self, var: Any, is_ok: bool = False) -> None:
        self.val = var
        self.is_ok = is_ok

    def set(self, value: Any, is_ok: bool = True):
        self.val = value
        self.is_ok = is_ok


class Share:
    lock = threading.Lock()
    p_amont_vl = DataItem(0.0)
    p_aval_vl = DataItem(0.0)
    pos_vl = DataItem(0.0)
    q_vl = DataItem(0.0)

    @classmethod
    def mbus_poll_thread(cls):
        """Modbus polling thread"""
        # init modbus client
        fmc = FloatModbusClient(host='localhost', port=502)
        # initialization of the polynomial to get Cv for a valve position (non-linear device)
        # coefs src: VL Oppy
        cv_poly = np.poly1d([-1.75115535e-10,  6.23498970e-08, -8.64511406e-06,  5.65364659e-04,
                             -1.61157646e-02,  1.79337632e-01,  7.87619448e-01, -3.60037881e-03])
        # polling loop
        while True:
            # do modbus reading on socket
            read_flt_l = fmc.read_float(0, 3)
            # if read is ok, store result in regs (with thread lock)
            with cls.lock:
                if read_flt_l:
                    cls.p_amont_vl.set(read_flt_l[0])
                    cls.p_aval_vl.set(read_flt_l[1])
                    cls.pos_vl.set(read_flt_l[2])
                    try:
                        cls.q_vl.set(valve_flow(abs(cv_poly(cls.pos_vl.val)), cls.p_amont_vl.val, cls.p_aval_vl.val))
                    except ValueError:
                        cls.q_vl.is_ok = False
                else:
                    cls.p_amont_vl.is_ok = False
                    cls.p_aval_vl.is_ok = False
                    cls.pos_vl.is_ok = False
                    cls.q_vl.is_ok = False
            # 1s before next polling
            time.sleep(1.0)


class HmiApp(tk.Tk):
    """Tk HMI app"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # configure main window
        self.wm_title('Nano HMI flow valve')
        # add canvas
        self.cvs = tk.Canvas(self, width=960, height=720)
        self.cvs.pack()
        # load background image
        self._photo_img = tk.PhotoImage(file='img/background.png')
        self.cvs.create_image(0, 0, anchor=tk.NW, image=self._photo_img)
        # add an overlay with text fields
        self.amt_txt = self.cvs.create_text(733, 340, font=('Helvetica', 36))
        self.avl_txt = self.cvs.create_text(227, 340, font=('Helvetica', 36))
        self.pos_txt = self.cvs.create_text(480, 530, font=('Helvetica', 36))
        self.qvl_txt = self.cvs.create_text(480, 660, font=('Helvetica', 36))
        # start widget update loop
        self.after(ms=500, func=self.txt_update_loop)
        # start csv export loop
        self.after(ms=2000, func=self.csv_export_loop)

    def txt_update_loop(self):
        # define widget update list
        widgets_l = [(self.amt_txt, '%.2f bars', Share.p_amont_vl),
                     (self.avl_txt, '%.2f bars', Share.p_aval_vl),
                     (self.pos_txt, '%.2f %%', Share.pos_vl),
                     (self.qvl_txt, 'Estimation débit VL %.0f nm3/h', Share.q_vl),]
        # update text widgets
        with Share.lock:
            for txt_wdg, txt_fmt, d_item in widgets_l:
                self.cvs.itemconfig(txt_wdg, text=txt_fmt % d_item.val)
                self.cvs.itemconfig(txt_wdg, fill='black' if d_item.is_ok else 'red')
        # refresh txt widgets in 500 ms
        self.after(ms=500, func=self.txt_update_loop)

    def csv_export_loop(self):
        try:
            with open('export.csv', 'a', newline='') as csv_file:
                # init CSV writer
                fields_l = ['datetime', 'p_amont', 'p_aval', 'position_vl', 'q_vl']
                csv_w = csv.DictWriter(csv_file, extrasaction='ignore', dialect='excel-fr',
                                       fieldnames=fields_l)
                # add headers for a new file
                if csv_file.tell() == 0:
                    csv_w.writeheader()
                # add current data items to the CSV
                csv_w.writerow({'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'p_amont': round(Share.p_amont_vl.val, 2),
                                'p_aval': round(Share.p_aval_vl.val, 2),
                                'position_vl': round(Share.pos_vl.val, 2),
                                'q_vl': round(Share.q_vl.val)})
        except PermissionError:
            pass
        # refresh csv every 10s
        self.after(ms=10_000, func=self.csv_export_loop)


if __name__ == '__main__':
    # add ExcelFr dialect to csv
    csv.register_dialect('excel-fr', ExcelFr())
    # set current directory to this place
    chdir(dirname(abspath(__file__)))
    # start modbus polling thread
    threading.Thread(target=Share.mbus_poll_thread, daemon=True).start()
    # main Tk App
    app = HmiApp()
    app.mainloop()

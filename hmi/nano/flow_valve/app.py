#!/usr/bin/python3

from collections import deque
import csv
from datetime import datetime
from os import chdir
from os.path import abspath, dirname
import time
import threading
from lib.modbus import FloatModbusClient
from lib.flow_coefficient import valve_flow
import numpy as np
import tkinter as tk


# some class
class ExcelFr(csv.excel):
    delimiter = ';'


class Share:
    lock = threading.Lock()
    p_amont_vl = None
    p_aval_vl = None
    pos_vl = None
    q_vl = None
    p_amont_vl_stack = deque(maxlen=360)
    p_aval_vl_stack = deque(maxlen=360)
    pos_vl_stack = deque(maxlen=360)
    q_vl_stack = deque(maxlen=360)

    @classmethod
    def mbus_poll_thread(cls):
        """Modbus polling thread"""
        # init modbus client
        fmc = FloatModbusClient(host='localhost', port=502)
        # initialization of the polynomial to get Cv for a valve position (non-linear device)
        # coefs src: VL Oppy
        cv_poly = np.poly1d([-1.75115535e-10,  6.23498970e-08, -8.64511406e-06,  5.65364659e-04,
                             -1.61157646e-02,  1.79337632e-01,  7.87619448e-01, -3.60037881e-03])
        # init stacks last feed time
        last_q_feed_t = time.monotonic()
        # polling loop
        while True:
            # do modbus reading on socket
            read_flt_l = fmc.read_float(0, 3)
            # if read is ok, store result in regs (with thread lock)
            with cls.lock:
                if read_flt_l:
                    cls.p_amont_vl = read_flt_l[0]
                    cls.p_aval_vl = read_flt_l[1]
                    cls.pos_vl = read_flt_l[2]
                    try:
                        cls.q_vl = (valve_flow(abs(cv_poly(cls.pos_vl)), cls.p_amont_vl, cls.p_aval_vl))
                    except (ValueError, TypeError):
                        cls.q_vl = None
                else:
                    cls.p_amont_vl = None
                    cls.p_aval_vl = None
                    cls.pos_vl = None
                    cls.q_vl = None
                # feed the stacks every 10s
                if time.monotonic() - last_q_feed_t > 10.0:
                    last_q_feed_t = time.monotonic()
                    Share.p_amont_vl_stack.append(Share.p_amont_vl)
                    Share.p_aval_vl_stack.append(Share.p_aval_vl)
                    Share.pos_vl_stack.append(Share.pos_vl)
                    Share.q_vl_stack.append(Share.q_vl)
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
        widgets_l = [(self.amt_txt, '%.2f bars', Share.p_amont_vl, 0.0),
                     (self.avl_txt, '%.2f bars', Share.p_aval_vl, 0.0),
                     (self.pos_txt, '%.2f %%', Share.pos_vl, 0.0),
                     (self.qvl_txt, 'Estimation débit VL %.0f nm3/h', Share.q_vl, 0),]
        # update text widgets
        with Share.lock:
            for wdg_txt, fmt, current_val, default_val in widgets_l:
                # fill text widget with current values or set text as red
                if current_val is None:
                    self.cvs.itemconfig(wdg_txt, fill='red')
                else:
                    self.cvs.itemconfig(wdg_txt, text=fmt % current_val)
                    self.cvs.itemconfig(wdg_txt, fill='black')
                # avoid empty text area
                if not self.cvs.itemcget(wdg_txt, 'text'):
                    self.cvs.itemconfig(wdg_txt, text=fmt % default_val)
        # refresh txt widgets in 500 ms
        self.after(ms=500, func=self.txt_update_loop)

    def csv_export_loop(self):
        # define the export list [(fieldname, value, nb of digits), ]
        export_l = [('p_amont', Share.p_amont_vl, 2), ('p_aval', Share.p_aval_vl, 2),
                    ('position_vl', Share.pos_vl, 2), ('q_vl', Share.q_vl, 0)]
        # build CSV export dict
        csv_d = dict()
        csv_d['datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with Share.lock:
            for fieldname, value, digits in export_l:
                try:
                    csv_d[fieldname] = round(value, digits) if digits else round(value)
                except TypeError:
                    csv_d[fieldname] = float('nan')
        try:
            with open('export.csv', 'a', newline='') as csv_file:
                # init CSV writer
                csv_w = csv.DictWriter(csv_file, extrasaction='ignore', dialect='excel-fr',
                                       fieldnames=csv_d.keys())
                # add headers for a new file
                if csv_file.tell() == 0:
                    csv_w.writeheader()
                # add current row
                csv_w.writerow(csv_d)
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

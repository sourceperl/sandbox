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
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from matplotlib import style


# some class
class ExcelFr(csv.excel):
    delimiter = ';'


class Share:
    lock = threading.Lock()
    p_amont_vl = None
    p_aval_vl = None
    pos_vl = None
    sp_p_aval = None
    q_vl = None
    p_amont_vl_stack = deque(maxlen=360)
    p_aval_vl_stack = deque(maxlen=360)
    pos_vl_stack = deque(maxlen=360)
    q_vl_stack = deque(maxlen=360)
    sp_p_aval_stack = deque(maxlen=360)

    @classmethod
    def mbus_poll_thread(cls):
        """Modbus polling thread"""
        # init modbus client
        fmc = FloatModbusClient(host='localhost', port=502, debug=False)
        # initialization of the polynomial to get Cv for a valve position (non-linear device)
        # coefs src: VL Oppy
        cv_poly = np.poly1d([-1.75115535e-10,  6.23498970e-08, -8.64511406e-06,  5.65364659e-04,
                             -1.61157646e-02,  1.79337632e-01,  7.87619448e-01, -3.60037881e-03])
        # init stacks last feed time
        last_q_feed_t = time.monotonic()
        # polling loop
        while True:
            # do modbus reading on socket
            rfloat_d = dict()
            for addr in (804, 808, 812, 816):
                result = fmc.read_float(addr)
                rfloat_d[addr] = result[0] if result is not None else None
            # if read is ok, store result in regs (with thread lock)
            with cls.lock:
                cls.p_amont_vl = rfloat_d.get(804)
                cls.p_aval_vl = rfloat_d.get(808)
                cls.pos_vl = rfloat_d.get(812)
                cls.sp_p_aval = rfloat_d.get(816)
                try:
                    cls.q_vl = (valve_flow(max(cv_poly(cls.pos_vl), 0.0), cls.p_amont_vl, cls.p_aval_vl))
                except (ValueError, TypeError):
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


class TrendPamontFrame(tk.Frame):
    # some const
    WIDTH = 400
    HEIGHT = 300
    DPI = 120

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # init matplotlib graph
        style.use('ggplot')
        self.fig = Figure(figsize=(self.WIDTH/self.DPI, self.HEIGHT/self.DPI), dpi=self.DPI)
        self.plt = self.fig.add_subplot()
        self.fig.set_tight_layout(True)
        # add animate graph widget to tk app
        graph = FigureCanvasTkAgg(self.fig, master=self)
        self.can_graph = graph.get_tk_widget()
        self.can_graph.pack()
        # init plot refresh function
        self.func_anim = FuncAnimation(self.fig, self.update_graph, interval=1000)

    def update_graph(self, _):
        # decrease CPU usage if not mapped
        if self.winfo_ismapped():
            self.plt.clear()
            self.plt.set_ylabel('bars')
            with Share.lock:
                self.plt.plot(Share.p_amont_vl_stack, 'r-')


class TrendPavalFrame(tk.Frame):
    # some const
    WIDTH = 400
    HEIGHT = 300
    DPI = 120

    def __init__(self, parent, *args, **kwargs):
        # heritage stuff
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # init matplotlib graph
        style.use('ggplot')
        self.fig = Figure(figsize=(self.WIDTH/self.DPI, self.HEIGHT/self.DPI), dpi=self.DPI)
        self.plt = self.fig.add_subplot()
        self.fig.set_tight_layout(True)
        # add animate graph widget to tk app
        graph = FigureCanvasTkAgg(self.fig, master=self)
        self.can_graph = graph.get_tk_widget()
        self.can_graph.pack()
        # init plot refresh function
        self.func_anim = FuncAnimation(self.fig, self.update_graph, interval=1000)

    def update_graph(self, _):
        # decrease CPU usage if not mapped
        if self.winfo_ismapped():
            self.plt.clear()
            self.plt.set_ylabel('bars')
            with Share.lock:
                self.plt.plot(Share.p_aval_vl_stack, 'b-')


class TabSyno(tk.Frame):
    """Synoptic tab class"""

    def __init__(self, parent, *args, **kwargs):
        # heritage stuff
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # add canvas
        self.cvs = tk.Canvas(self, width=960, height=720)
        self.cvs.pack()
        # load background image
        self._photo_img = tk.PhotoImage(file='img/background.png')
        self.cvs.create_image(0, 0, anchor=tk.NW, image=self._photo_img)
        # add an overlay with text fields
        self.amt_txt = self.cvs.create_text(733, 430, font=('Helvetica', 36))
        self.avl_txt = self.cvs.create_text(227, 430, font=('Helvetica', 36))
        self.pos_txt = self.cvs.create_text(480, 610, font=('Helvetica', 36))
        self.qvl_txt = self.cvs.create_text(480, 680, font=('Helvetica', 36))
        # embed matplotlib frame in canvas
        self.fr_gph_amt = TrendPamontFrame(self)
        self.cvs.create_window(750, 175, window=self.fr_gph_amt)
        self.fr_gph_avl = TrendPavalFrame(self)
        self.cvs.create_window(200, 175, window=self.fr_gph_avl)
        # start widget update loop
        self.after(ms=500, func=self.txt_update_loop)

    def txt_update_loop(self):
        # decrease CPU usage if not mapped
        if self.winfo_ismapped():
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


class TabGraph(tk.Frame):
    # some const
    WIDTH = 960
    HEIGHT = 720
    DPI = 120

    def __init__(self, parent, *args, **kwargs):
        # heritage stuff
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # init matplotlib graph
        style.use('ggplot')
        self.fig = Figure(figsize=(self.WIDTH/self.DPI, self.HEIGHT/self.DPI), dpi=self.DPI)
        self.plt_h = self.fig.add_subplot(211)
        self.plt_b = self.fig.add_subplot(212)
        self.plt_h.set_title('Historique pressions')
        self.plt_h.set_ylabel('bars')
        self.plt_b.set_title('Historique position VL')
        self.plt_b.set_ylabel('%')
        self.fig.set_tight_layout(True)
        # add animate graph widget to tk app
        graph = FigureCanvasTkAgg(self.fig, master=self)
        self.can_graph = graph.get_tk_widget()
        self.can_graph.pack()
        # init plot refresh function
        self.func_anim = FuncAnimation(self.fig, self.update_graph, interval=1000)

    def update_graph(self, _):
        # decrease CPU usage if not mapped
        if self.winfo_ismapped():
            self.plt_h.clear()
            self.plt_h.set_title('Historique pressions')
            self.plt_h.set_ylabel('bars')
            self.plt_b.clear()
            self.plt_b.set_title('Historique position VL')
            self.plt_b.set_ylabel('%')
            with Share.lock:
                self.plt_h.plot(Share.p_amont_vl_stack, 'r-')
                self.plt_h.plot(Share.p_aval_vl_stack, 'b-')
                self.plt_b.plot(Share.pos_vl_stack, 'g-')


class HmiApp(tk.Tk):
    """Tk HMI app"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # configure main window
        self.wm_title('Nano HMI flow valve')
        # build a notebook with tabs
        self.note = ttk.Notebook(self)
        self.tab_syno = TabSyno(self.note)
        self.tab_graph = TabGraph(self.note)
        self.note.add(self.tab_syno, text='Synoptique (F1)')
        self.note.add(self.tab_graph, text='Graphiques (F2)')
        self.note.pack(fill=tk.BOTH, expand=True)
        # defaut selected tab
        self.note.select(self.tab_syno)
        # bind function keys to tabs
        self.bind('<F1>', lambda evt: self.note.select(self.tab_syno))
        self.bind('<F2>', lambda evt: self.note.select(self.tab_graph))
        # add an exit button
        self.but_exit = tk.Button(self, text="Exit", padx=25, command=lambda: self.destroy())
        self.but_exit.pack(side=tk.RIGHT, padx=10, pady=5)
        # start csv export loop
        self.after(ms=2000, func=self.csv_export_loop)

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
        # add CSV export dict data to 'export.csv' file
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

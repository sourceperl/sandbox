#!/usr/bin/env python

"""
Pressure regulation simulator with a PID controller
"""

from collections import deque
from random import random
from os import chdir
from os.path import abspath, dirname
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
from lib.pid import PID
from lib.misc import valve_flow


# some class
class ControlValveFlow:
    """A class to calculate the flow in a control valve from its Cv curve"""

    def __init__(self):
        # adjust the polynomial to model the CV for all the operating points of the valve
        # a list of reference points extracted from the data sheet of the valve
        ref_pts_l = [(0, 0), (4, 5), (10, 15), (16, 21), (20, 25), (30, 40), (40, 75),
                     (50, 145), (53, 166), (60, 235), (70, 345), (80, 460), (90, 580), (100, 680)]
        # fitting a seventh-order polynomial with this points
        x_ref, y_ref = zip(*ref_pts_l)
        self._cv_poly = np.poly1d(np.polyfit(x_ref, y_ref, deg=7))

    def get_cv(self, position: float):
        return self._cv_poly(position)

    def get_nm3(self, position: float,  p1_bara: float, p2_bara: float):
        return valve_flow(cv=self.get_cv(position), p1_bara=p1_bara, p2_bara=p2_bara)


class SimGasRegulator:
    """A class to modelize gas network with pressure drop in a control valve"""

    def __init__(self):
        # public
        self.p_up = 0.0
        self.water_vol_m3 = 0
        self.delay_s = 0.0
        self.gas_stock_m3 = self.p_up * self.water_vol_m3
        self.gas_leak_m3 = 0
        self.vlv_flow = ControlValveFlow()
        # private
        self._delay_queue = deque()

    def clear(self):
        self.p_up = 0.0
        self.water_vol_m3 = 0
        self.delay_s = 0.0
        self.gas_stock_m3 = self.p_up * self.water_vol_m3
        self.gas_leak_m3 = 0
        self._delay_queue.clear()

    def update(self, valve_position, dt_s):
        # create a delta stock
        # flow in vavle increase gas stock
        flow_nm3_h = self.vlv_flow.get_nm3(position=valve_position, p1_bara=self.p_up, p2_bara=self.p_down)
        delta_stock_m3 = (flow_nm3_h/3600) * dt_s
        # consumption decrease gas stock
        delta_stock_m3 -= (self.gas_leak_m3/3600) * dt_s
        # push delta stock to delay queue
        self._delay_queue.append(delta_stock_m3)
        # apply delta stock with delay to current stock
        while (len(self._delay_queue) > self.delay_s/dt_s):
            self.gas_stock_m3 += self._delay_queue.popleft()

    @property
    def p_down(self):
        return self.gas_stock_m3/self.water_vol_m3


class TabGraph(tk.Frame):
    # some const
    WIDTH = 960
    HEIGHT = 720
    DPI = 120

    def __init__(self, parent, *args, **kwargs):
        # heritage stuff
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # init Sim object
        self.sim_gas_reg = SimGasRegulator()
        # some tk vars
        self.var_sim_t = tk.DoubleVar(self, value=4.0)
        self.var_p_up = tk.DoubleVar(self, value=58.0)
        self.var_p_down = tk.DoubleVar(value=43.0)
        self.var_sp_p_down = tk.DoubleVar(value=44.0)
        self.var_pos_t0 = tk.DoubleVar(value=37.0)
        self.var_vlv_hyst = tk.DoubleVar(value=0.75)
        self.var_water_vol = tk.DoubleVar(value=2_500)
        self.var_gas_leak = tk.DoubleVar(value=44_000)
        self.var_delay_s = tk.DoubleVar(value=20.0)
        self.var_kp = tk.DoubleVar(value=1.0)
        self.var_ti = tk.DoubleVar(value=15)
        self.var_td = tk.DoubleVar(value=float('+inf'))
        self.var_sim_t.trace_add('write', lambda *_: self._valid_form())
        self.var_p_up.trace_add('write', lambda *_: self._valid_form())
        self.var_p_down.trace_add('write', lambda *_: self._valid_form())
        self.var_sp_p_down.trace_add('write', lambda *_: self._valid_form())
        self.var_pos_t0.trace_add('write', lambda *_: self._valid_form())
        self.var_vlv_hyst.trace_add('write', lambda *_: self._valid_form())
        self.var_water_vol.trace_add('write', lambda *_: self._valid_form())
        self.var_gas_leak.trace_add('write', lambda *_: self._valid_form())
        self.var_delay_s.trace_add('write', lambda *_: self._valid_form())
        self.var_kp.trace_add('write', lambda *_: self._valid_form())
        self.var_ti.trace_add('write', lambda *_: self._valid_form())
        self.var_td.trace_add('write', lambda *_: self._valid_form())
        # init matplotlib graph
        style.use('ggplot')
        self.fig = Figure(figsize=(self.WIDTH/self.DPI, self.HEIGHT/self.DPI), dpi=self.DPI)
        self.plt_h = self.fig.add_subplot(211)
        self.plt_b = self.fig.add_subplot(212)
        self.fig.set_tight_layout(True)
        # add animate graph widget to tk app
        self.graph = FigureCanvasTkAgg(self.fig, master=self)
        self.can_graph = self.graph.get_tk_widget()
        self.can_graph.grid(row=0, column=0)
        # add parameters frame
        self.fr_param = tk.Frame(self)
        self.fr_param.grid(row=0, column=1, sticky=tk.N)
        self.btn_run = tk.Button(self.fr_param, text="Simulation", padx=30, command=self.run_sim)
        self.btn_run.pack(padx=10, pady=10)
        # sim time
        self.lbl_sim_t = tk.Label(self.fr_param, text="Temps de simulation (h)")
        self.lbl_sim_t.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_sim_t = tk.Entry(self.fr_param, textvariable=self.var_sim_t)
        self.ent_sim_t.pack(padx=10, pady=2)
        # p up
        self.lbl_p_up = tk.Label(self.fr_param, text="P amont (BarA)")
        self.lbl_p_up.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_p_up = tk.Entry(self.fr_param, textvariable=self.var_p_up)
        self.ent_p_up.pack(padx=10, pady=2)
        # p down
        self.lbl_p_down = tk.Label(self.fr_param, text="P aval (BarA)")
        self.lbl_p_down.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_p_down = tk.Entry(self.fr_param, textvariable=self.var_p_down)
        self.ent_p_down.pack(padx=10, pady=2)
        # p down
        self.lbl_sp_p_down = tk.Label(self.fr_param, text="Consigne P aval (BarA)")
        self.lbl_sp_p_down.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_sp_p_down = tk.Entry(self.fr_param, textvariable=self.var_sp_p_down)
        self.ent_sp_p_down.pack(padx=10, pady=2)
        # position at t=0
        self.lbl_pos_t0 = tk.Label(self.fr_param, text="Position VL pour t=0s (%)")
        self.lbl_pos_t0.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_pos_t0 = tk.Entry(self.fr_param, textvariable=self.var_pos_t0)
        self.ent_pos_t0.pack(padx=10, pady=2)
        # valve hysteresis
        self.lbl_vlv_hyst = tk.Label(self.fr_param, text="Hystérésis de vanne (%)")
        self.lbl_vlv_hyst.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_vlv_hyst = tk.Entry(self.fr_param, textvariable=self.var_vlv_hyst)
        self.ent_vlv_hyst.pack(padx=10, pady=2)
        # water volume
        self.lbl_w_vol = tk.Label(self.fr_param, text="Volume en eau (m3)")
        self.lbl_w_vol.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_w_vol = tk.Entry(self.fr_param, textvariable=self.var_water_vol)
        self.ent_w_vol.pack(padx=10, pady=2)
        # gas leak
        self.lbl_g_leak = tk.Label(self.fr_param, text="Consommation (nm3/h)")
        self.lbl_g_leak.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_g_leak = tk.Entry(self.fr_param, textvariable=self.var_gas_leak)
        self.ent_g_leak.pack(padx=10, pady=2)
        # delay
        self.lbl_delay_s = tk.Label(self.fr_param, text="Delais de reponse process (s)")
        self.lbl_delay_s.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_delay_s = tk.Entry(self.fr_param, textvariable=self.var_delay_s)
        self.ent_delay_s.pack(padx=10, pady=2)
        # kp
        self.lbl_kp = tk.Label(self.fr_param, text="PID Kp")
        self.lbl_kp.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_kp = tk.Entry(self.fr_param, textvariable=self.var_kp)
        self.ent_kp.pack(padx=10, pady=2)
        # ti
        self.lbl_ti = tk.Label(self.fr_param, text="PID Ti (s)")
        self.lbl_ti.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_ti = tk.Entry(self.fr_param, textvariable=self.var_ti)
        self.ent_ti.pack(padx=10, pady=2)
        # td
        self.lbl_td = tk.Label(self.fr_param, text="PID Td (s)")
        self.lbl_td.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_td = tk.Entry(self.fr_param, textvariable=self.var_td)
        self.ent_td.pack(padx=10, pady=2)
        # Q VL
        self.lbl_valve_f = tk.Label(self.fr_param)
        self.lbl_valve_f.pack(padx=10, pady=20, anchor=tk.CENTER)
        # init form at startup
        self._valid_form()

    @classmethod
    def _nvar_is_valid(cls, tk_var: tk.Variable, f_min: float = 0.0, f_max: float = 100.0):
        try:
            if not (f_min <= tk_var.get() <= f_max):
                raise ValueError
            return True
        except (ValueError, tk.TclError):
            return False

    @classmethod
    def _entry_anim(cls, tk_entry: tk.Entry, valid: bool):
        tk_entry.config(bg='white' if valid else 'red')

    def _valid_form(self):
        # simulation time
        sim_t_valid = self._nvar_is_valid(self.var_sim_t, 0.0, 10.0)
        self._entry_anim(self.ent_sim_t, sim_t_valid)
        # p up
        p_up_valid = self._nvar_is_valid(self.var_p_up, 0.0, 100.0)
        self._entry_anim(self.ent_p_up, p_up_valid)
        # p down
        p_down_valid = self._nvar_is_valid(self.var_p_down, 0.0, 100.0)
        self._entry_anim(self.ent_p_down, p_down_valid)
        # set point p down
        sp_p_down_valid = self._nvar_is_valid(self.var_sp_p_down, 0.0, 100.0)
        self._entry_anim(self.ent_sp_p_down, sp_p_down_valid)
        # position at t=0s
        pos_t0_valid = self._nvar_is_valid(self.var_pos_t0, 0.0, 100.0)
        self._entry_anim(self.ent_pos_t0, pos_t0_valid)
        # valve hysteresis
        vlv_hyst_valid = self._nvar_is_valid(self.var_vlv_hyst, 0.0, 50.0)
        self._entry_anim(self.ent_vlv_hyst, vlv_hyst_valid)
        # water volume
        water_vol_valid = self._nvar_is_valid(self.var_water_vol, 0, 100_000)
        self._entry_anim(self.ent_w_vol, water_vol_valid)
        # gas leak
        gas_leak_valid = self._nvar_is_valid(self.var_gas_leak, 0, 100_000)
        self._entry_anim(self.ent_g_leak, gas_leak_valid)
        # output delay
        delay_s_valid = self._nvar_is_valid(self.var_delay_s, 0.0, 1000.0)
        self._entry_anim(self.ent_delay_s, delay_s_valid)
        # PID kp
        kp_valid = self._nvar_is_valid(self.var_kp, 0.0, 1000.0)
        self._entry_anim(self.ent_kp, kp_valid)
        # PID ti
        ti_valid = self._nvar_is_valid(self.var_ti, 0.0, float('+inf'))
        self._entry_anim(self.ent_ti, ti_valid)
        # PID td
        td_valid = self._nvar_is_valid(self.var_td, 0.0, float('+inf'))
        self._entry_anim(self.ent_td, td_valid)
        # flow in valve
        try:
            vcv = self.sim_gas_reg.vlv_flow.get_cv(self.var_pos_t0.get())
            vflow = self.sim_gas_reg.vlv_flow.get_nm3(self.var_pos_t0.get(), self.var_p_up.get(), self.var_p_down.get())
        except tk.TclError:
            vcv = float('nan')
            vflow = float('nan')
        self.lbl_valve_f.config(text=f'Cv = {vcv:.0f}\nDébit VL = {vflow:_.0f} nm3/h')
        # run button
        form_is_valid = sim_t_valid and p_up_valid and p_down_valid and sp_p_down_valid and pos_t0_valid and \
            vlv_hyst_valid and water_vol_valid and gas_leak_valid and delay_s_valid and kp_valid and \
            ti_valid and td_valid
        self.btn_run.configure(state='normal' if form_is_valid else 'disabled')

    def run_sim(self):
        # keep track of values for plotting
        sp_l, pv_l, time_l, out_l = [], [], [], []

        # set process simulator values
        self.sim_gas_reg.clear()
        self.sim_gas_reg.p_up = self.var_p_up.get()
        self.sim_gas_reg.delay_s = self.var_delay_s.get()
        self.sim_gas_reg.water_vol_m3 = self.var_water_vol.get()
        self.sim_gas_reg.gas_stock_m3 = self.var_water_vol.get() * self.var_p_down.get()
        self.sim_gas_reg.gas_leak_m3 = self.var_gas_leak.get()

        # init PID with pv = sp at startup
        kp = self.var_kp.get()
        ti = self.var_ti.get()
        td = self.var_td.get()
        ki = 1/ti
        kd = 1/td
        sp_p_down = self.var_sp_p_down.get()
        vlv_hyst = self.var_vlv_hyst.get()
        # start at PID at t0 valve position
        pid = PID(kp=kp, ki=ki, kd=kd, output_limits=(0, 100), setpoint=self.sim_gas_reg.p_down, auto_mode=False)
        pid.set_auto_mode(enabled=True, last_output=self.var_pos_t0.get())
        physical_pos = self.var_pos_t0.get()

        # simulation vars
        sim_t_s = self.var_sim_t.get() * 3600
        step_s = 1.0
        total_s = round(sim_t_s/step_s)

        # run PID simulation
        for secs in [x * step_s for x in range(0, total_s)]:
            # update upstream pressure
            #if secs > total_s/2:
            #    self.sim_gas_reg.p_up += 0.00

            # fix set point on time line
            if secs == total_s/2:
                pid.setpoint = sp_p_down

            # add some noise (max 0.01%) to p_down measure view by PID to reflect real process values
            p_down = self.sim_gas_reg.p_down
            p_down += p_down * .0001 * random()

            # update PID and valve
            pid_pos = pid(input_=p_down, dt=step_s)

            # reflect PID output to physical if absolut move is greater than hyst
            if abs(physical_pos - pid_pos) > vlv_hyst:
                physical_pos = pid_pos

            self.sim_gas_reg.update(physical_pos, dt_s=step_s)

            # fill plotting arrays
            time_l += [secs]
            out_l += [physical_pos]
            pv_l += [p_down]
            sp_l += [pid.setpoint]

        # plotting
        self.plt_h.clear()
        self.plt_h.grid(visible=True)
        self.plt_h.set_ylabel('Pression (barA)')
        self.plt_h.plot(time_l, pv_l, label='P aval')
        self.plt_h.plot(time_l, sp_l, label='Consigne')
        self.plt_h.legend()
        self.plt_b.clear()
        self.plt_b.grid(visible=True)
        self.plt_b.set_xlabel('Temps (s)')
        self.plt_b.set_ylabel('Ouverture (%)')
        self.plt_b.plot(time_l, out_l, label='Position vanne')
        self.plt_b.legend()
        self.graph.draw()


class HmiApp(tk.Tk):
    """Tk HMI app"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # configure main window
        self.wm_title('Simulateur gaz')
        # build a notebook with tabs
        self.note = ttk.Notebook(self)
        self.tab_graph = TabGraph(self.note)
        self.note.add(self.tab_graph, text='PID pression aval (F1)')
        self.note.grid(row=0, padx=2, pady=2)
        # defaut selected tab
        self.note.select(self.tab_graph)
        # bind function keys to tabs
        self.bind('<F1>', lambda evt: self.note.select(self.tab_graph))
        # add an exit button
        self.but_exit = tk.Button(self, text="Exit", padx=25, command=self.destroy)
        self.but_exit.grid(row=1, padx=10, pady=5, sticky=tk.E)


if __name__ == '__main__':
    # set current directory to this place
    chdir(dirname(abspath(__file__)))
    # main Tk App
    app = HmiApp()
    app.mainloop()

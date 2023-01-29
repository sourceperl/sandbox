#!/usr/bin/env python

"""
CV and flow calculation GUI for process control valve.
"""

import math
import tkinter as tk


# some const
VLD_CV_COEFS = [-0.003600378815220472, 0.7876194476782555, 0.17933763182740164, -0.016115764610012975,
                0.000565364659464521, -8.645114062181e-06, 6.2349896989e-08, -1.75115535e-10]


# some functions
def celsius_to_kelvin(deg_c: float) -> float:
    """Conversion from degree Celsius to Kelvin"""
    return deg_c + 273.15


def is_subsonic(p_up_bara: float, p_down_bara: float) -> bool:
    """Obtain subsonic state for current pressures"""
    return p_down_bara > p_up_bara / 2


def valve_flow(cv: float, p1_bara: float, p2_bara: float, t_deg_c: float = 6.0, sg: float = 0.554) -> float:
    """Compute flow rate (nm3/h) in a valve from it's Cv"""
    # check args value
    if p1_bara < 0.00:
        raise ValueError('arg p1_bara must be positive')
    if p2_bara < 0.00:
        raise ValueError('arg p2_bara must be positive')
    # formats args for calculation
    t_k = celsius_to_kelvin(t_deg_c)
    sign = 1 if p1_bara - p2_bara >= 0 else -1
    p_up = max(p1_bara, p2_bara)
    p_down = min(p1_bara, p2_bara)
    dp = p_up - p_down
    # circulation below or over critical point
    if is_subsonic(p_up, p_down):
        return sign * 417 * cv * p_up * (1 - ((2 * dp) / (3 * p_up))) * math.sqrt(dp / (p_up * sg * t_k))
    else:
        return sign * 0.471 * 417 * cv * p_up * math.sqrt(1 / (sg * t_k))


# some class
class ControlValve:
    """A control valve model class."""

    def __init__(self, coef_l: list = []):
        self.coef_l = coef_l

    def get_cv(self, position: float):
        result = 0.0
        for n, a in enumerate(self.coef_l):
            result += a * position**n
        return round(result)

    def get_nm3(self, position: float, p1_bara: float, p2_bara: float):
        return valve_flow(cv=self.get_cv(position), p1_bara=p1_bara, p2_bara=p2_bara)


class TabFlowRate(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # heritage stuff
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # init control valve
        self.ctrl_valve = ControlValve(coef_l=VLD_CV_COEFS)
        # some tk vars
        self.var_p_up = tk.DoubleVar(self, value=58.0)
        self.var_p_down = tk.DoubleVar(value=43.0)
        self.var_pos = tk.DoubleVar(value=37.0)
        self.var_p_up.trace_add('write', lambda *_: self._valid_form())
        self.var_p_down.trace_add('write', lambda *_: self._valid_form())
        self.var_pos.trace_add('write', lambda *_: self._valid_form())
        # p up
        self.lbl_p_up = tk.Label(self, text="P amont (BarA)")
        self.lbl_p_up.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_p_up = tk.Entry(self, textvariable=self.var_p_up)
        self.ent_p_up.pack(padx=10, pady=2)
        # p down
        self.lbl_p_down = tk.Label(self, text="P aval (BarA)")
        self.lbl_p_down.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_p_down = tk.Entry(self, textvariable=self.var_p_down)
        self.ent_p_down.pack(padx=10, pady=2)
        # position
        self.lbl_pos_t0 = tk.Label(self, text="Position VL (%)")
        self.lbl_pos_t0.pack(padx=10, pady=2, anchor=tk.W)
        self.ent_pos_t0 = tk.Entry(self, textvariable=self.var_pos)
        self.ent_pos_t0.pack(padx=10, pady=2)
        # Separate form and results area
        tk.Label(self).pack(pady=5)
        # Cv and flow labels
        self.lbl_valve_cv = tk.Label(self)
        self.lbl_valve_cv.pack(padx=10, pady=5, anchor=tk.CENTER)
        self.lbl_valve_flow = tk.Label(self)
        self.lbl_valve_flow.pack(padx=10, pady=5, anchor=tk.CENTER)
        # init form at startup
        self._valid_form()

    @classmethod
    def _nvar_is_valid(cls, tk_var: tk.Variable, f_min: float = 0.0, f_max: float = 100.0) -> bool:
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
        # p up
        p_up_valid = self._nvar_is_valid(self.var_p_up, 0.0, 100.0)
        self._entry_anim(self.ent_p_up, p_up_valid)
        # p down
        p_down_valid = self._nvar_is_valid(self.var_p_down, 0.0, 100.0)
        self._entry_anim(self.ent_p_down, p_down_valid)
        # position at t=0s
        pos_valid = self._nvar_is_valid(self.var_pos, 0.0, 100.0)
        self._entry_anim(self.ent_pos_t0, pos_valid)
        # check form validity
        form_invalid = not (p_up_valid and p_down_valid and pos_valid)
        # flow in valve
        try:
            if form_invalid:
                raise ValueError
            valve_cv = self.ctrl_valve.get_cv(self.var_pos.get())
            valve_nm3 = self.ctrl_valve.get_nm3(
                self.var_pos.get(), p1_bara=self.var_p_up.get(), p2_bara=self.var_p_down.get())
        except (tk.TclError, ValueError):
            self.lbl_valve_cv.config(text='Cv = nan')
            self.lbl_valve_flow.config(text='Débit VL = nan')
        else:
            self.lbl_valve_cv.config(text=f'Cv = {valve_cv:.0f}')
            self.lbl_valve_flow.config(text=f'Débit VL = {valve_nm3:_.0f} nm3/h'.replace('_', ' '))


class HmiApp(tk.Tk):
    """Tk HMI app"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # configure main window
        self.wm_title('Calcul de débit VL')
        # build a notebook with tabs
        self.tab_graph = TabFlowRate(self)
        self.tab_graph.grid(row=0)
        # add an exit button
        self.but_exit = tk.Button(self, text="Exit", padx=25, command=self.destroy)
        self.but_exit.grid(row=1, padx=10, pady=10, sticky=tk.EW)


if __name__ == '__main__':
    # main Tk App
    app = HmiApp()
    app.mainloop()

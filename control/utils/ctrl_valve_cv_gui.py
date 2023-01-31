#!/usr/bin/env python

"""
CV and flow calculation GUI for process control valve.
"""

import math
import tkinter as tk
from tkinter import ttk


# some const
VL_POS_CV_MAP = [(0, 0), (4, 5), (10, 15), (16, 21), (20, 25), (30, 40), (40, 75), (50, 145), (53, 166), (60, 235),
                 (70, 345), (80, 460), (90, 580), (100, 680)]


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


def valve_cv(q_nm3: float, p1_bara: float, p2_bara: float, t_deg_c: float = 6.0, sg: float = 0.554) -> float:
    """Compute Cv of a valve from it's flow rate (nm3/h)"""
    # check args value
    if q_nm3 < 0.00:
        raise ValueError('arg q_nm3 must be positive')
    if p1_bara < 0.00:
        raise ValueError('arg p1_bara must be positive')
    if p2_bara < 0.00:
        raise ValueError('arg p2_bara must be positive')
    # formats args for calculation
    t_k = celsius_to_kelvin(t_deg_c)
    p_up = max(p1_bara, p2_bara)
    p_down = min(p1_bara, p2_bara)
    dp = p_up - p_down
    # circulation below or over critical point
    if is_subsonic(p_up, p_down):
        return q_nm3 / (417 * p_up * (1 - ((2 * dp) / (3 * p_up))) * math.sqrt(dp / (p_up * sg * t_k)))
    else:
        return q_nm3 / (0.471 * 417 * p_up * math.sqrt(1 / (sg * t_k)))


def tk_var_valid(tk_var: tk.Variable, f_min: float = 0.0, f_max: float = 100.0) -> bool:
    try:
        if not (f_min <= tk_var.get() <= f_max):
            raise ValueError
        return True
    except (ValueError, tk.TclError):
        return False


def tk_entry_anim(tk_entry: tk.Entry, valid: bool) -> None:
    tk_entry.config(bg='white' if valid else 'red')


def vl_pos2cv(position: float) -> float:
    origin_pos, origin_cv = VL_POS_CV_MAP[0]
    for ref_pos, ref_cv in VL_POS_CV_MAP:
        if position <= ref_pos:
            res_cv = origin_cv
            if ref_pos - origin_pos > 0.0:
                res_cv += (ref_cv - origin_cv) * (position - origin_pos) / (ref_pos - origin_pos)
            return res_cv
        origin_pos, origin_cv = ref_pos, ref_cv
    return origin_cv


def vl_cv2pos(cv: float) -> float:
    origin_pos, origin_cv = VL_POS_CV_MAP[0]
    for ref_pos, ref_cv in VL_POS_CV_MAP:
        if cv <= ref_cv:
            res_pos = origin_pos
            if ref_cv - origin_cv > 0:
                res_pos += (ref_pos - origin_pos) * (cv - origin_cv) / (ref_cv - origin_cv)
            return res_pos
        origin_pos, origin_cv = ref_pos, ref_cv
    return origin_pos


# some class
class TabCv2Flow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # heritage stuff
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # some tk vars
        self.var_p_up = tk.DoubleVar(self, value=60.0)
        self.var_p_down = tk.DoubleVar(self, value=50.0)
        self.var_cv = tk.IntVar(self, value=680)
        self.var_p_up.trace_add('write', lambda *_: self._valid_form())
        self.var_p_down.trace_add('write', lambda *_: self._valid_form())
        self.var_cv.trace_add('write', lambda *_: self._valid_form())
        # p up
        self.lbl_p_up = tk.Label(self, text='P amont (BarA)')
        self.lbl_p_up.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_p_up = tk.Entry(self, textvariable=self.var_p_up)
        self.ent_p_up.pack(padx=10, pady=5)
        # p down
        self.lbl_p_down = tk.Label(self, text='P aval (BarA)')
        self.lbl_p_down.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_p_down = tk.Entry(self, textvariable=self.var_p_down)
        self.ent_p_down.pack(padx=10, pady=5)
        # cv
        self.lbl_cv = tk.Label(self, text='Cv')
        self.lbl_cv.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_cv = tk.Entry(self, textvariable=self.var_cv)
        self.ent_cv.pack(padx=10, pady=5)
        # separate form and results area
        tk.Label(self).pack(pady=20)
        # Cv and flow labels
        self.lbl_valve_flow = tk.Label(self)
        self.lbl_valve_flow.pack(padx=10, pady=5, anchor=tk.CENTER)
        # init form at startup
        self._valid_form()

    def _valid_form(self):
        # p up
        p_up_valid = tk_var_valid(self.var_p_up, 0.0, 100.0)
        tk_entry_anim(self.ent_p_up, p_up_valid)
        # p down
        p_down_valid = tk_var_valid(self.var_p_down, 0.0, 100.0)
        tk_entry_anim(self.ent_p_down, p_down_valid)
        # cv
        cv_valid = tk_var_valid(self.var_cv, 0, 2400)
        tk_entry_anim(self.ent_cv, cv_valid)
        # check form validity
        form_invalid = not (p_up_valid and p_down_valid and cv_valid)
        # flow in valve
        try:
            if form_invalid:
                raise ValueError
            valve_nm3 = valve_flow(self.var_cv.get(), p1_bara=self.var_p_up.get(), p2_bara=self.var_p_down.get())
        except (tk.TclError, ValueError):
            self.lbl_valve_flow.config(text='Débit = nan')
        else:
            self.lbl_valve_flow.config(text=f'Débit = {valve_nm3:_.0f} nm3/h'.replace('_', ' '))


class TabFlow2Cv(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # heritage stuff
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # some tk vars
        self.var_p_up = tk.DoubleVar(self, value=60.0)
        self.var_p_down = tk.DoubleVar(self, value=50.0)
        self.var_q = tk.DoubleVar(self, value=496_472.0)
        self.var_p_up.trace_add('write', lambda *_: self._valid_form())
        self.var_p_down.trace_add('write', lambda *_: self._valid_form())
        self.var_q.trace_add('write', lambda *_: self._valid_form())
        # p up
        self.lbl_p_up = tk.Label(self, text='P amont (BarA)')
        self.lbl_p_up.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_p_up = tk.Entry(self, textvariable=self.var_p_up)
        self.ent_p_up.pack(padx=10, pady=5)
        # p down
        self.lbl_p_down = tk.Label(self, text='P aval (BarA)')
        self.lbl_p_down.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_p_down = tk.Entry(self, textvariable=self.var_p_down)
        self.ent_p_down.pack(padx=10, pady=5)
        # position
        self.lbl_q = tk.Label(self, text='Débit (nm3/h)')
        self.lbl_q.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_pos = tk.Entry(self, textvariable=self.var_q)
        self.ent_pos.pack(padx=10, pady=5)
        # separate form and results area
        tk.Label(self).pack(pady=20)
        # Cv and flow labels
        self.lbl_valve_cv = tk.Label(self)
        self.lbl_valve_cv.pack(padx=10, pady=5, anchor=tk.CENTER)
        self.lbl_valve_pos = tk.Label(self)
        self.lbl_valve_pos.pack(padx=10, pady=5, anchor=tk.CENTER)
        # init form at startup
        self._valid_form()

    def _valid_form(self):
        # p up
        p_up_valid = tk_var_valid(self.var_p_up, 0.0, 100.0)
        tk_entry_anim(self.ent_p_up, p_up_valid)
        # p down
        p_down_valid = tk_var_valid(self.var_p_down, 0.0, 100.0)
        tk_entry_anim(self.ent_p_down, p_down_valid)
        # flow
        q_valid = tk_var_valid(self.var_q, 0, 5_000_000)
        tk_entry_anim(self.ent_pos, q_valid)
        # check form validity
        form_invalid = not (p_up_valid and p_down_valid and q_valid)
        # flow in valve
        try:
            if form_invalid:
                raise ValueError
            cv = valve_cv(self.var_q.get(), p1_bara=self.var_p_up.get(), p2_bara=self.var_p_down.get())
        except (tk.TclError, ValueError):
            self.lbl_valve_cv.config(text='Cv = nan')
        else:
            self.lbl_valve_cv.config(text=f'Cv = {cv:.0f}')


class TabPos2Flow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # heritage stuff
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # some tk vars
        self.var_p_up = tk.DoubleVar(self, value=60.0)
        self.var_p_down = tk.DoubleVar(self, value=50.0)
        self.var_pos = tk.DoubleVar(self, value=100.0)
        self.var_p_up.trace_add('write', lambda *_: self._valid_form())
        self.var_p_down.trace_add('write', lambda *_: self._valid_form())
        self.var_pos.trace_add('write', lambda *_: self._valid_form())
        # p up
        self.lbl_p_up = tk.Label(self, text='P amont (BarA)')
        self.lbl_p_up.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_p_up = tk.Entry(self, textvariable=self.var_p_up)
        self.ent_p_up.pack(padx=10, pady=5)
        # p down
        self.lbl_p_down = tk.Label(self, text='P aval (BarA)')
        self.lbl_p_down.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_p_down = tk.Entry(self, textvariable=self.var_p_down)
        self.ent_p_down.pack(padx=10, pady=5)
        # position
        self.lbl_pos = tk.Label(self, text='Position VL (%)')
        self.lbl_pos.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_pos = tk.Entry(self, textvariable=self.var_pos)
        self.ent_pos.pack(padx=10, pady=5)
        # separate form and results area
        tk.Label(self).pack(pady=10)
        # Cv and flow labels
        self.lbl_valve_cv = tk.Label(self)
        self.lbl_valve_cv.pack(padx=10, pady=5, anchor=tk.CENTER)
        self.lbl_valve_flow = tk.Label(self)
        self.lbl_valve_flow.pack(padx=10, pady=5, anchor=tk.CENTER)
        txt = 'Utilise le tableau "VL_POS_CV_MAP" pour définir le profil position/Cv de la VL.'
        self.lbl_comment = tk.Label(self, font=('', 10, 'italic'), text=txt)
        self.lbl_comment.pack(padx=10, pady=5, anchor=tk.CENTER)
        # init form at startup
        self._valid_form()

    def _valid_form(self):
        # p up
        p_up_valid = tk_var_valid(self.var_p_up, 0.0, 100.0)
        tk_entry_anim(self.ent_p_up, p_up_valid)
        # p down
        p_down_valid = tk_var_valid(self.var_p_down, 0.0, 100.0)
        tk_entry_anim(self.ent_p_down, p_down_valid)
        # position
        pos_valid = tk_var_valid(self.var_pos, 0.0, 100.0)
        tk_entry_anim(self.ent_pos, pos_valid)
        # check form validity
        form_invalid = not (p_up_valid and p_down_valid and pos_valid)
        # flow in valve
        try:
            if form_invalid:
                raise ValueError
            valve_cv = vl_pos2cv(self.var_pos.get())
            valve_nm3 = valve_flow(cv=valve_cv, p1_bara=self.var_p_up.get(), p2_bara=self.var_p_down.get())
        except (tk.TclError, ValueError):
            self.lbl_valve_cv.config(text='Cv = nan')
            self.lbl_valve_flow.config(text='Débit = nan')
        else:
            self.lbl_valve_cv.config(text=f'Cv = {valve_cv:_.0f}')
            self.lbl_valve_flow.config(text=f'Débit = {valve_nm3:_.0f} nm3/h'.replace('_', ' '))


class TabFlow2Pos(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        # heritage stuff
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # some tk vars
        self.var_p_up = tk.DoubleVar(self, value=60.0)
        self.var_p_down = tk.DoubleVar(self, value=50.0)
        self.var_flow = tk.DoubleVar(self, value=496472.0)
        self.var_p_up.trace_add('write', lambda *_: self._valid_form())
        self.var_p_down.trace_add('write', lambda *_: self._valid_form())
        self.var_flow.trace_add('write', lambda *_: self._valid_form())
        # p up
        self.lbl_p_up = tk.Label(self, text='P amont (BarA)')
        self.lbl_p_up.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_p_up = tk.Entry(self, textvariable=self.var_p_up)
        self.ent_p_up.pack(padx=10, pady=5)
        # p down
        self.lbl_p_down = tk.Label(self, text='P aval (BarA)')
        self.lbl_p_down.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_p_down = tk.Entry(self, textvariable=self.var_p_down)
        self.ent_p_down.pack(padx=10, pady=5)
        # flow
        self.lbl_flow = tk.Label(self, text='Débit (nm3/h)')
        self.lbl_flow.pack(padx=10, pady=5, anchor=tk.W)
        self.ent_flow = tk.Entry(self, textvariable=self.var_flow)
        self.ent_flow.pack(padx=10, pady=5)
        # separate form and results area
        tk.Label(self).pack(pady=10)
        # Cv and flow labels
        self.lbl_valve_cv = tk.Label(self)
        self.lbl_valve_cv.pack(padx=10, pady=5, anchor=tk.CENTER)
        self.lbl_valve_pos = tk.Label(self)
        self.lbl_valve_pos.pack(padx=10, pady=5, anchor=tk.CENTER)
        txt = 'Utilise le tableau "VL_POS_CV_MAP" pour définir le profil position/Cv de la VL.'
        self.lbl_comment = tk.Label(self, font=('', 10, 'italic'), text=txt)
        self.lbl_comment.pack(padx=10, pady=5, anchor=tk.CENTER)
        # init form at startup
        self._valid_form()

    def _valid_form(self):
        # p up
        p_up_valid = tk_var_valid(self.var_p_up, 0.0, 100.0)
        tk_entry_anim(self.ent_p_up, p_up_valid)
        # p down
        p_down_valid = tk_var_valid(self.var_p_down, 0.0, 100.0)
        tk_entry_anim(self.ent_p_down, p_down_valid)
        # flow
        flow_valid = tk_var_valid(self.var_flow, 0.0, 5_000_000.0)
        tk_entry_anim(self.ent_flow, flow_valid)
        # check form validity
        form_invalid = not (p_up_valid and p_down_valid and flow_valid)
        # flow in valve
        try:
            if form_invalid:
                raise ValueError
            cv = valve_cv(q_nm3=self.var_flow.get(), p1_bara=self.var_p_up.get(), p2_bara=self.var_p_down.get())
            pos = vl_cv2pos(cv)
        except (tk.TclError, ValueError):
            self.lbl_valve_cv.config(text='Cv = nan')
            self.lbl_valve_pos.config(text='Position = nan')
        else:
            self.lbl_valve_cv.config(text=f'Cv = {cv:.0f}')
            self.lbl_valve_pos.config(text=f'Position = {pos:.2f} %')


class HmiApp(tk.Tk):
    """Tk HMI app"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # configure main window
        self.wm_title('Calcul Cv vanne de régulation')
        self.geometry('600x400')
        self.resizable(width=False, height=False)
        # build a notebook with tabs
        self.note = ttk.Notebook(self)
        self.tab_cv2flow = TabCv2Flow(self.note)
        self.tab_flow2cv = TabFlow2Cv(self.note)
        self.tab_pos2flow = TabPos2Flow(self.note)
        self.tab_flow2pos = TabFlow2Pos(self.note)
        self.note.add(self.tab_cv2flow, text='Cv -> débit (F1)')
        self.note.add(self.tab_flow2cv, text='Débit -> Cv (F2)')
        self.note.add(self.tab_pos2flow, text='Position -> débit (F3)')
        self.note.add(self.tab_flow2pos, text='Débit -> position (F4)')
        self.note.pack(fill=tk.BOTH, expand=True)
        # defaut selected tab
        self.note.select(self.tab_cv2flow)
        # bind function keys to tabs
        self.bind('<F1>', lambda evt: self.note.select(self.tab_cv2flow))
        self.bind('<F2>', lambda evt: self.note.select(self.tab_flow2cv))
        self.bind('<F3>', lambda evt: self.note.select(self.tab_pos2flow))
        self.bind('<F4>', lambda evt: self.note.select(self.tab_flow2pos))
        # add an exit button
        self.but_exit = tk.Button(self, text='Exit', padx=25, command=self.destroy)
        self.but_exit.pack(padx=10, pady=10, side=tk.RIGHT)


if __name__ == '__main__':
    # main Tk App
    app = HmiApp()
    app.mainloop()

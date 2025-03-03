import tkinter as tk
from tkinter import ttk

from .conf import AppConf


# some functions
def hs_to_mj(hs_kwh: float) -> float:
    """Convert Hs from kwh/nm3 to MJ/nm3."""
    return hs_kwh * 3.6


def hs_to_t25(hs_t0: float) -> float:
    """Convert Hs from t_comb = 0°C to 25 °C."""
    return hs_t0 * 0.997_4


def to_kelvin(celsius: float) -> float:
    """Converts temperature from Celsius to Kelvin."""
    return celsius + 273.15


def to_celsius(kelvin: float) -> float:
    """Converts temperature from Kelvin to Celsius."""
    return kelvin - 273.15


def set_grid_conf(widget: ttk.Frame) -> None:
    """Apply global geometry to this frame (maintain uniform geometry across the entire frame)."""
    widget.columnconfigure(0, minsize=450)
    widget.columnconfigure(1, minsize=450)
    widget.rowconfigure(0, minsize=265)
    widget.rowconfigure(1, minsize=265)


# some class
class TabTemplate(ttk.Frame):
    def __init__(self, master: tk.Tk, app_conf: AppConf, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        # global tk app shortcuts
        self.tk_app = master
        self.app_conf = app_conf

    def _valid_int(self, new_value: str, widget_name: str) -> bool:
        for char in new_value:
            if char not in '+0123456789':
                return False
        # validate numeric entry
        try:
            int(new_value)
            self.nametowidget(widget_name).config(style='TEntry')
        except ValueError:
            self.nametowidget(widget_name).config(style='Red.TEntry')
        return True

    def _valid_float(self, new_value: str, widget_name: str) -> bool:
        # reject invalid char
        for char in new_value:
            if char not in '+-.0123456789':
                return False
        # validate numeric entry
        try:
            float(new_value)
            self.nametowidget(widget_name).config(style='TEntry')
        except ValueError:
            self.nametowidget(widget_name).config(style='Red.TEntry')
        return True

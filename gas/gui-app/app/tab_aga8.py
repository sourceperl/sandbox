import tkinter as tk
import traceback
from tkinter import ttk

from aga8.AGA8 import AGA8Detail

from .conf import AppConf
from .const import PRES_REF, TEMP_REF_K
from .misc import hs_to_mj, hs_to_t25, to_kelvin


class TabAGA8(tk.Frame):
    def __init__(self, master: tk.Tk, app_conf: AppConf, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        # global tk app shortcuts
        self.tk_app = master
        self.app_conf = app_conf
        # style for red background
        style = ttk.Style()
        style.configure('Red.TEntry', fieldbackground='red')

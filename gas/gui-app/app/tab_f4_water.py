import tkinter as tk
import traceback
from tkinter import ttk

from .conf import AppConf
from .misc import set_grid_conf


class TabWater(ttk.Frame):
    def __init__(self, master: tk.Tk, app_conf: AppConf, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        # global tk app shortcuts
        self.tk_app = master
        self.app_conf = app_conf

        # uniform geometry for this frame
        set_grid_conf(self)

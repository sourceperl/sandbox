import argparse
import tkinter as tk
from tkinter import ttk

from .__version__ import __version__
from .conf import AppConf
from .const import APP_NAME
from .tab_f1_sgerg import TabSGERG
from .tab_f2_aga8 import TabAGA8
from .tab_f3_pcs import TabPCS
from .tab_f4_water import TabWater


class App(tk.Tk):
    def __init__(self, app_conf: AppConf, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # global tk conf
        self.title(f'{APP_NAME} - V{__version__}')
        self.geometry('900x560')
        self.resizable(width=False, height=False)
        # ensure global ttk style is default
        self.style = ttk.Style()
        self.style.theme_use('default')
        # add a custom style for TEntry with syntax fault
        self.style.configure('Red.TEntry', fieldbackground='red')
        # build a notebook with tabs
        self.note = ttk.Notebook(self)
        self.tab_sgerg = TabSGERG(self, app_conf)
        self.tab_aga8 = TabAGA8(self, app_conf)
        self.tab_pcs = TabPCS(self, app_conf)
        self.tab_water = TabWater(self, app_conf)
        self.note.add(self.tab_sgerg, text='SGERG (F1)')
        self.note.add(self.tab_aga8, text='AGA8 (F2)')
        self.note.add(self.tab_pcs, text='ISO-6976 (PCS) (F3)')
        self.note.add(self.tab_water, text='Teneur en eau (F4)')
        self.note.pack(fill=tk.BOTH, expand=True)
        # defaut selected tab
        self.note.select(self.tab_sgerg)
        # bind function keys to tabs
        self.bind('<F1>', lambda evt: self.note.select(self.tab_sgerg))
        self.bind('<F2>', lambda evt: self.note.select(self.tab_aga8))
        self.bind('<F3>', lambda evt: self.note.select(self.tab_pcs))
        self.bind('<F4>', lambda evt: self.note.select(self.tab_water))


def main():
    # parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, help='turn on debug')
    args = parser.parse_args()
    # init app conf
    app_conf = AppConf()
    app_conf.debug = args.debug
    # start app
    app = App(app_conf)
    app.mainloop()

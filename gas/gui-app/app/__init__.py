import argparse
import tkinter as tk
from tkinter import ttk


from .conf import AppConf
from .tab_sgerg import TabSGERG
from .tab_aga8 import TabAGA8



class App(tk.Tk):
    def __init__(self, app_conf: AppConf, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title('My App')
        # build a notebook with tabs
        self.note = ttk.Notebook(self)
        self.tab_sgerg = TabSGERG(self, app_conf)
        self.tab_aga8 = TabAGA8(self, app_conf)
        self.note.add(self.tab_sgerg, text='SGERG (F1)')
        self.note.add(self.tab_aga8, text='AGA8 (F2)')
        self.note.pack(fill=tk.BOTH, expand=True)
        # defaut selected tab
        self.note.select(self.tab_sgerg)
        # bind function keys to tabs
        self.bind('<F1>', lambda evt: self.note.select(self.tab_sgerg))
        self.bind('<F2>', lambda evt: self.note.select(self.tab_aga8))


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

import re
import tkinter as tk
from tkinter import ttk

from aga8 import AGA8
from sgerg import SGERG_88


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('My App')
        # style for red background
        style = ttk.Style()
        style.configure('Red.TEntry', fieldbackground='red')
        # variables to store entry values
        self.pcs_var = tk.StringVar(value='12400')
        self.density_var = tk.StringVar(value='0.600')
        # create and place widgets
        self.create_widgets()

    def _allow_int(self, new_value: str, widget_name: str):
        valid = new_value == '' or new_value.isdigit()
        # valid = new_value == '' or re.match(r'^[a-zA-Z\s]*$', new_value) is not None
        self.nametowidget(widget_name).config(style='Red.TEntry' if not valid else 'TEntry')
        return True

    def _allow_float(self, new_value: str, widget_name: str):
        valid = new_value == '' or new_value.isdigit()
        # valid = new_value == '' or re.match(r'^[a-zA-Z\s]*$', new_value) is not None
        self.nametowidget(widget_name).config(style='Red.TEntry' if not valid else 'TEntry')
        return True

    def create_widgets(self):
        """Create and place widgets."""
        # PCS entry
        ttk.Label(self, text='PCS:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._allow_int), '%P', '%W')
        self.pcs_entry = ttk.Entry(self, textvariable=self.pcs_var, validate='key', validatecommand=v_cmd)
        self.pcs_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        # density entry
        ttk.Label(self, text='Densité:').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._allow_float), '%P', '%W')
        self.pcs_entry = ttk.Entry(self, textvariable=self.density_var, validate='key', validatecommand=v_cmd)
        self.pcs_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        # submit button
        sub_button = ttk.Button(self, text='Submit', command=self.submit)
        sub_button.grid(row=4, column=0, columnspan=2, pady=10)
        #
        #self.columnconfigure(1, weight=1)

    def submit(self):
        try:
            print('PCS:     ', self.pcs_var.get())
            print('Densité: ', self.density_var.get())
        except tk.TclError as e:
            raise e


def main():
    app = App()
    app.mainloop()

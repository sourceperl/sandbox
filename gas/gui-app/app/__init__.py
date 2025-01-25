import re
import tkinter as tk
from tkinter import ttk

from aga8 import AGA8
from sgerg.SGERG_88 import SGERG


# some functions
def hs_to_mj(hs_kwh: float) -> float:
    """Convert Hs from kwh/nm3 to MJ/nm3."""
    return hs_kwh * 3.6


def hs_to_t25(hs_t0: float) -> float:
    """Convert Hs from t_comb = 0°C to 25 °C."""
    return hs_t0 * 0.997_4


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('My App')
        # style for red background
        style = ttk.Style()
        style.configure('Red.TEntry', fieldbackground='red')
        # default gas composition
        self.pcs = 11_320
        self.density = 0.581
        self.x_co2 = 0.006
        self.x_h2 = 0.0
        # create and place widgets
        self.create_widgets()
        # populate SGERG results widgets for default gas composition
        self._sgerg_compute()

    def _valid_pcs(self, new_value: str):
        try:
            self.pcs = int(new_value)
            self.pcs_entry.config(style='TEntry')
        except ValueError:
            self.pcs_entry.config(style='Red.TEntry')
        else:
            self._sgerg_compute()
        return True

    def _valid_density(self, new_value: str):
        # valid = new_value == '' or re.match(r'^[a-zA-Z\s]*$', new_value) is not None
        try:
            self.density = float(new_value)
            self.density_entry.config(style='TEntry')
        except ValueError:
            self.density_entry.config(style='Red.TEntry')
        else:
            self._sgerg_compute()
        return True

    def _sgerg_compute(self):
        try:
            # french PCS k(wh/nm3, t_comb = 0 °C) to SGERG Hs (MJ/nm3, t_comb = 25 °C)
            hs_t25 = hs_to_t25(self.pcs/1000)
            hs_t25_mj = hs_to_mj(hs_t25)
            # do SGERG
            sgerg = SGERG(hs=hs_t25_mj, d=self.density, x_co2=self.x_co2, x_h2=self.x_h2)
            z, _ = sgerg.run(p_bar=60.0, t_celsius=16.85)
            # update Z field
            self.z_var.set(f'{z:.04f}')
        except:
            # update Z field
            self.z_var.set('n/a')

    def create_widgets(self):
        """Create and place widgets."""
        # variables to store entry values
        self.pcs_var = tk.StringVar(value=f'{self.pcs}')
        self.density_var = tk.StringVar(value=f'{self.density:.3f}')
        self.z_var = tk.StringVar()
        # PCS entry
        ttk.Label(self, text='PCS:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_pcs), '%P')
        self.pcs_entry = ttk.Entry(self, textvariable=self.pcs_var, validate='key', validatecommand=v_cmd)
        self.pcs_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        # density entry
        ttk.Label(self, text='Densité:').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_density), '%P')
        self.density_entry = ttk.Entry(self, textvariable=self.density_var, validate='key', validatecommand=v_cmd)
        self.density_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        # Z entry
        ttk.Label(self, text='Z:').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.density_entry = ttk.Entry(self, textvariable=self.z_var, state='readonly')
        self.density_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        # submit button
        # sub_button = ttk.Button(self, text='Submit', command=self.submit)
        # sub_button.grid(row=4, column=0, columnspan=2, pady=10)


def main():
    app = App()
    app.mainloop()

import tkinter as tk
from tkinter import ttk

from sgerg.SGERG_88 import SGERG

from .misc import hs_to_mj, hs_to_t25


class TabSGERG(tk.Frame):
    def __init__(self, master: tk.Tk, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        # global tk app shortcuts
        self.tk_app = master
        # style for red background
        style = ttk.Style()
        style.configure('Red.TEntry', fieldbackground='red')
        # default gas composition
        self.pcs = 11_320
        self.density = 0.581
        self.x_co2 = 0.006
        self.x_h2 = 0.0
        # create and place widgets
        self._add_widgets()
        # populate SGERG results widgets for default gas composition
        self._sgerg_compute()

    def _valid_pcs(self, new_value: str):
        try:
            self.pcs = int(new_value)
            self.ent_pcs.config(style='TEntry')
        except ValueError:
            self.ent_pcs.config(style='Red.TEntry')
        else:
            self._sgerg_compute()
        return True

    def _valid_density(self, new_value: str):
        # valid = new_value == '' or re.match(r'^[a-zA-Z\s]*$', new_value) is not None
        try:
            self.density = float(new_value)
            self.ent_dens.config(style='TEntry')
        except ValueError:
            self.ent_dens.config(style='Red.TEntry')
        else:
            self._sgerg_compute()
        return True

    def _valid_x_co2(self, new_value: str):
        try:
            self.x_co2 = float(new_value)
            self.ent_x_co2.config(style='TEntry')
        except ValueError:
            self.ent_x_co2.config(style='Red.TEntry')
        else:
            self._sgerg_compute()
        return True

    def _valid_x_h2(self, new_value: str):
        try:
            self.x_h2 = float(new_value)
            self.ent_x_h2.config(style='TEntry')
        except ValueError:
            self.ent_x_h2.config(style='Red.TEntry')
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
            z, rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
            # update result fields
            self.sv_z.set(f'{z:.04f}')
            self.sv_rho_m.set(f'{rho_m:.04f}')
        except:
            # update result fields
            self.sv_z.set('n/a')
            self.sv_rho_m.set('n/a')

    def _add_widgets(self):
        """Create and place widgets."""
        # variables to store entry values
        self.sv_pcs = tk.StringVar(value=f'{self.pcs}')
        self.sv_dens = tk.StringVar(value=f'{self.density:.3f}')
        self.sv_x_co2 = tk.StringVar(value=f'{self.x_co2:.3f}')
        self.sv_x_h2 = tk.StringVar(value=f'{self.x_h2:.3f}')
        self.sv_z = tk.StringVar()
        self.sv_rho_m = tk.StringVar()

        # main label frames
        self.fm_in = ttk.LabelFrame(self, text='Entrées')
        self.fm_in.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N)
        self.fm_out = ttk.LabelFrame(self, text='Résultats')
        self.fm_out.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)

        # inputs frame
        # PCS entry
        ttk.Label(self.fm_in, text='PCS:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_pcs), '%P')
        self.ent_pcs = ttk.Entry(self.fm_in, textvariable=self.sv_pcs,
                                 validate='key', validatecommand=v_cmd, width=10)
        self.ent_pcs.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_in, text='w/m3').grid(row=0, column=2, padx=5, pady=5, sticky='w')
        # density entry
        ttk.Label(self.fm_in, text='Densité:').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_density), '%P')
        self.ent_dens = ttk.Entry(self.fm_in, textvariable=self.sv_dens,
                                  validate='key', validatecommand=v_cmd, width=10)
        self.ent_dens.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        # x_co2 entry
        ttk.Label(self.fm_in, text='Fraction molaire CO2:').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_x_co2), '%P')
        self.ent_x_co2 = ttk.Entry(self.fm_in, textvariable=self.sv_x_co2,
                                   validate='key', validatecommand=v_cmd, width=10)
        self.ent_x_co2.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        # x_h2 entry
        ttk.Label(self.fm_in, text='Fraction molaire H2:').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_x_h2), '%P')
        self.ent_x_h2 = ttk.Entry(self.fm_in, textvariable=self.sv_x_h2,
                                  validate='key', validatecommand=v_cmd, width=10)
        self.ent_x_h2.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        # outputs frame
        # Z entry
        ttk.Label(self.fm_out, text='Z:').grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.ent_z = ttk.Entry(self.fm_out, textvariable=self.sv_z, state='readonly', width=10)
        self.ent_z.grid(row=0, column=5, padx=5, pady=5, sticky='ew')
        # Rho m entry
        ttk.Label(self.fm_out, text='\N{GREEK SMALL LETTER RHO}m:').grid(row=1, column=4, padx=5, pady=5, sticky='w')
        self.ent_rho_m = ttk.Entry(self.fm_out, textvariable=self.sv_rho_m, state='readonly', width=10)
        self.ent_rho_m.grid(row=1, column=5, padx=5, pady=5, sticky='ew')
        # submit button
        # sub_button = ttk.Button(self, text='Submit', command=self.submit)
        # sub_button.grid(row=4, column=0, columnspan=2, pady=10)

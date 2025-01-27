import tkinter as tk
from tkinter import ttk

from sgerg.SGERG_88 import SGERG

from .misc import hs_to_mj, hs_to_t25, to_kelvin

# some const
PRES_REF = 1.01325
TEMP_REF_K = 273.15


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
        # default pressure and temperature
        self.p_bar = 60.0
        self.t_celsius = 16.85
        self.volume_raw = 1000.0
        # create and place widgets
        self._add_widgets()
        # populate SGERG results widgets for default gas composition
        self._update_results()

    def _valid_pcs(self, new_value: str):
        try:
            self.pcs = int(new_value)
            self.ent_pcs.config(style='TEntry')
        except ValueError:
            self.ent_pcs.config(style='Red.TEntry')
        else:
            self._update_results()
        return True

    def _valid_density(self, new_value: str):
        # valid = new_value == '' or re.match(r'^[a-zA-Z\s]*$', new_value) is not None
        try:
            self.density = float(new_value)
            self.ent_dens.config(style='TEntry')
        except ValueError:
            self.ent_dens.config(style='Red.TEntry')
        else:
            self._update_results()
        return True

    def _valid_x_co2(self, new_value: str):
        try:
            self.x_co2 = float(new_value)
            self.ent_x_co2.config(style='TEntry')
        except ValueError:
            self.ent_x_co2.config(style='Red.TEntry')
        else:
            self._update_results()
        return True

    def _valid_x_h2(self, new_value: str):
        try:
            self.x_h2 = float(new_value)
            self.ent_x_h2.config(style='TEntry')
        except ValueError:
            self.ent_x_h2.config(style='Red.TEntry')
        else:
            self._update_results()
        return True

    def _valid_pres(self, new_value: str):
        try:
            self.p_bar = float(new_value)
            self.ent_pres.config(style='TEntry')
        except ValueError:
            self.ent_pres.config(style='Red.TEntry')
        else:
            self._update_results()
        return True

    def _valid_temp(self, new_value: str):
        try:
            self.t_celsius = float(new_value)
            self.ent_temp.config(style='TEntry')
        except ValueError:
            self.ent_temp.config(style='Red.TEntry')
        else:
            self._update_results()
        return True

    def _valid_volume_raw(self, new_value: str):
        try:
            self.volume_raw = float(new_value)
            self.ent_vol.config(style='TEntry')
        except ValueError:
            self.ent_vol.config(style='Red.TEntry')
        else:
            self._update_results()
        return True

    def _update_results(self):
        try:
            # french PCS k(wh/nm3, t_comb = 0 °C) to SGERG Hs (MJ/nm3, t_comb = 25 °C)
            hs_t25 = hs_to_t25(self.pcs/1000)
            hs_t25_mj = hs_to_mj(hs_t25)
            # do SGERG
            sgerg = SGERG(hs=hs_t25_mj, d=self.density, x_co2=self.x_co2, x_h2=self.x_h2)
            z, rho_m = sgerg.run(p_bar=self.p_bar, t_celsius=self.t_celsius)
            z0, _ = sgerg.run(p_bar=1.01325, t_celsius=0.0)
            c_coef = self.p_bar/PRES_REF * TEMP_REF_K/to_kelvin(self.t_celsius) * z0/z
            # update result fields
            self.sv_z.set(f'{z:.04f}')
            self.sv_z_z0.set(f'{z/z0:.04f}')
            self.sv_z0_z.set(f'{z0/z:.04f}')
            self.sv_rho_m.set(f'{rho_m:.04f}')
            self.sv_c_coef.set(f'{c_coef:.04f}')
            self.sv_vol_cor.set(f'{self.volume_raw * c_coef:_.0f}'.replace('_', ' '))
        except:
            # update result fields
            self.sv_z.set('n/a')
            self.sv_z_z0.set('n/a')
            self.sv_z0_z.set('n/a')
            self.sv_rho_m.set('n/a')
            self.sv_c_coef.set('n/a')

    def _add_widgets(self):
        """Create and place widgets."""
        # variables to store entry values
        self.sv_pcs = tk.StringVar(value=f'{self.pcs}')
        self.sv_dens = tk.StringVar(value=f'{self.density:.3f}')
        self.sv_x_co2 = tk.StringVar(value=f'{self.x_co2:.3f}')
        self.sv_x_h2 = tk.StringVar(value=f'{self.x_h2:.3f}')
        self.sv_pres = tk.StringVar(value=f'{self.p_bar:.2f}')
        self.sv_temp = tk.StringVar(value=f'{self.t_celsius:.2f}')
        self.sv_vol_raw = tk.StringVar(value=f'{self.volume_raw:.2f}')
        self.sv_z = tk.StringVar()
        self.sv_z_z0 = tk.StringVar()
        self.sv_z0_z = tk.StringVar()
        self.sv_rho_m = tk.StringVar()
        self.sv_c_coef = tk.StringVar()
        self.sv_vol_cor = tk.StringVar()

        # composition frame
        self.fm_comp = ttk.LabelFrame(self, text='Composition')
        self.fm_comp.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_comp.columnconfigure(0, minsize=160)
        # PCS entry
        row = 0
        ttk.Label(self.fm_comp, text='PCS:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_pcs), '%P')
        self.ent_pcs = ttk.Entry(self.fm_comp, textvariable=self.sv_pcs,
                                 validate='key', validatecommand=v_cmd, width=10)
        self.ent_pcs.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='watts/m\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # density entry
        row += 1
        ttk.Label(self.fm_comp, text='Densité:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_density), '%P')
        self.ent_dens = ttk.Entry(self.fm_comp, textvariable=self.sv_dens,
                                  validate='key', validatecommand=v_cmd, width=10)
        self.ent_dens.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # x_co2 entry
        row += 1
        ttk.Label(self.fm_comp, text='Fraction molaire CO2:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_x_co2), '%P')
        self.ent_x_co2 = ttk.Entry(self.fm_comp, textvariable=self.sv_x_co2,
                                   validate='key', validatecommand=v_cmd, width=10)
        self.ent_x_co2.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # x_h2 entry
        row += 1
        ttk.Label(self.fm_comp, text='Fraction molaire H2:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_x_h2), '%P')
        self.ent_x_h2 = ttk.Entry(self.fm_comp, textvariable=self.sv_x_h2,
                                  validate='key', validatecommand=v_cmd, width=10)
        self.ent_x_h2.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

        # metering frame
        self.fm_met = ttk.LabelFrame(self, text='Comptage')
        self.fm_met.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_met.columnconfigure(0, minsize=160)
        # pressure entry
        row = 0
        ttk.Label(self.fm_met, text='Pression:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_pres), '%P')
        self.ent_pres = ttk.Entry(self.fm_met, textvariable=self.sv_pres,
                                  validate='key', validatecommand=v_cmd, width=10)
        self.ent_pres.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_met, text='bara').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # temperature entry
        row += 1
        ttk.Label(self.fm_met, text='Temperature:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_temp), '%P')
        self.ent_temp = ttk.Entry(self.fm_met, textvariable=self.sv_temp,
                                  validate='key', validatecommand=v_cmd, width=10)
        self.ent_temp.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_met, text='°C').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # volume entry
        row += 1
        ttk.Label(self.fm_met, text='Volume:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        v_cmd = (self.register(self._valid_volume_raw), '%P')
        self.ent_vol = ttk.Entry(self.fm_met, textvariable=self.sv_vol_raw,
                                 validate='key', validatecommand=v_cmd, width=10)
        self.ent_vol.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_met, text='m\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')

        # results frame
        self.fm_res = ttk.LabelFrame(self, text='Résultats')
        self.fm_res.grid(row=0, rowspan=2, column=1, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_res.columnconfigure(0, minsize=100)
        # Z entry
        row = 0
        ttk.Label(self.fm_res, text='Z:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_z = ttk.Entry(self.fm_res, textvariable=self.sv_z, state='readonly', width=10)
        self.ent_z.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # Z/Z0 entry
        row += 1
        ttk.Label(self.fm_res, text='Z/Z0:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_z_z0 = ttk.Entry(self.fm_res, textvariable=self.sv_z_z0, state='readonly', width=10)
        self.ent_z_z0.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # Z0/Z entry
        row += 1
        ttk.Label(self.fm_res, text='Z0/Z:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_z0_z = ttk.Entry(self.fm_res, textvariable=self.sv_z0_z, state='readonly', width=10)
        self.ent_z0_z.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # Rho m entry
        row += 1
        ttk.Label(self.fm_res, text='\N{GREEK SMALL LETTER RHO}m:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_rho_m = ttk.Entry(self.fm_res, textvariable=self.sv_rho_m, state='readonly', width=10)
        self.ent_rho_m.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # vertical space
        row += 1
        ttk.Label(self.fm_res, text='').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        # C entry
        row += 1
        ttk.Label(self.fm_res, text='Coefficient C:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_c = ttk.Entry(self.fm_res, textvariable=self.sv_c_coef, state='readonly', width=10)
        self.ent_c.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # vertical space
        row += 1
        ttk.Label(self.fm_res, text='').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        # corrected flow entry
        row += 1
        ttk.Label(self.fm_res, text='Volume corrigé:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_c_flow = ttk.Entry(self.fm_res, textvariable=self.sv_vol_cor, state='readonly', width=10)
        self.ent_c_flow.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res, text='nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')

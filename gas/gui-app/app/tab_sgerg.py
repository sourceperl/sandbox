import tkinter as tk
import traceback
from tkinter import ttk

from SGERG_88 import SGERG

from .conf import AppConf
from .const import PRES_REF, TEMP_REF_C, TEMP_REF_K
from .misc import hs_to_mj, hs_to_t25, to_kelvin

# some local const
INIT_PCS = 11_540
INIT_DENSITY = 0.610
INIT_CO2 = 0.69
INIT_H2 = 0.0
INIT_PRES = 60.0
INIT_TEMP = 16.85
INIT_RAW_VOL = 1000.0


class TabSGERG(ttk.Frame):
    def __init__(self, master: tk.Tk, app_conf: AppConf, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        # global tk app shortcuts
        self.tk_app = master
        self.app_conf = app_conf

        # fix geometry of this frame
        self.columnconfigure(0, minsize=400)
        self.columnconfigure(1, minsize=350)
        self.rowconfigure(0, minsize=250)
        self.rowconfigure(1, minsize=150)

        # variables to store ttk.Entry IN values (with write handlers)
        self.field_pcs = tk.StringVar(value=f'{INIT_PCS}')
        self.field_pcs.trace_add('write', self._on_fields_update)
        self.field_dens = tk.StringVar(value=f'{INIT_DENSITY:.3f}')
        self.field_dens.trace_add('write', self._on_fields_update)
        self.field_co2 = tk.StringVar(value=f'{INIT_CO2:.2f}')
        self.field_co2.trace_add('write', self._on_fields_update)
        self.field_h2 = tk.StringVar(value=f'{INIT_H2:.2f}')
        self.field_h2.trace_add('write', self._on_fields_update)
        self.field_pres = tk.StringVar(value=f'{INIT_PRES:.2f}')
        self.field_pres.trace_add('write', self._on_fields_update)
        self.field_temp = tk.StringVar(value=f'{INIT_TEMP:.2f}')
        self.field_temp.trace_add('write', self._on_fields_update)
        self.field_vol_raw = tk.StringVar(value=f'{INIT_RAW_VOL:.2f}')
        self.field_vol_raw.trace_add('write', self._on_fields_update)
        # variables to store ttk.Entry OUT values
        self.field_z = tk.StringVar()
        self.field_z0 = tk.StringVar()
        self.field_z_z0 = tk.StringVar()
        self.field_z0_z = tk.StringVar()
        self.field_c_coef = tk.StringVar()
        self.field_vol_cor = tk.StringVar()

        # add ttk.Entry widget commands for validation
        v_int_cmd = (self.register(self._valid_int), '%P', '%W')
        v_float_cmd = (self.register(self._valid_float), '%P', '%W')

        # create and place widgets
        # composition frame
        self.fm_comp = ttk.LabelFrame(self, text='Composition')
        self.fm_comp.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_comp.columnconfigure(0, minsize=160)
        # PCS entry
        row = 0
        ttk.Label(self.fm_comp, text='PCS (à 0 °C):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_pcs = ttk.Entry(self.fm_comp, textvariable=self.field_pcs,
                                 validate='key', validatecommand=v_int_cmd, width=10)
        self.ent_pcs.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # density entry
        row += 1
        ttk.Label(self.fm_comp, text='Densité:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_dens = ttk.Entry(self.fm_comp, textvariable=self.field_dens,
                                  validate='key', validatecommand=v_float_cmd, width=10)
        self.ent_dens.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # co2 entry
        row += 1
        ttk.Label(self.fm_comp, text='Fraction molaire CO2:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_co2 = ttk.Entry(self.fm_comp, textvariable=self.field_co2,
                                 validate='key', validatecommand=v_float_cmd, width=10)
        self.ent_co2.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # h2 entry
        row += 1
        ttk.Label(self.fm_comp, text='Fraction molaire H2:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_h2 = ttk.Entry(self.fm_comp, textvariable=self.field_h2,
                                validate='key', validatecommand=v_float_cmd, width=10)
        self.ent_h2.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')

        # metering frame
        self.fm_met = ttk.LabelFrame(self, text='Comptage')
        self.fm_met.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_met.columnconfigure(0, minsize=160)
        # pressure entry
        row = 0
        ttk.Label(self.fm_met, text='Pression:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_pres = ttk.Entry(self.fm_met, textvariable=self.field_pres,
                                  validate='key', validatecommand=v_float_cmd, width=10)
        self.ent_pres.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_met, text='bara').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # temperature entry
        row += 1
        ttk.Label(self.fm_met, text='Temperature:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_temp = ttk.Entry(self.fm_met, textvariable=self.field_temp,
                                  validate='key', validatecommand=v_float_cmd, width=10)
        self.ent_temp.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_met, text='°C').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # volume entry
        row += 1
        ttk.Label(self.fm_met, text='Volume mesureur:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_vol = ttk.Entry(self.fm_met, textvariable=self.field_vol_raw,
                                 validate='key', validatecommand=v_float_cmd, width=10)
        self.ent_vol.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_met, text='m\u00b3 (brut)').grid(row=row, column=2, padx=5, pady=5, sticky='w')

        # compressibility factor frame
        self.fm_z = ttk.LabelFrame(self, text='Facteur de compressibilité')
        self.fm_z.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_z.columnconfigure(0, minsize=125)
        # Z entry
        row = 0
        ttk.Label(self.fm_z, text='Z:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_z = ttk.Entry(self.fm_z, textvariable=self.field_z, state='readonly', width=10)
        self.ent_z.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # Z0 entry
        row += 1
        ttk.Label(self.fm_z, text='Z0:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_z0 = ttk.Entry(self.fm_z, textvariable=self.field_z0, state='readonly', width=10)
        self.ent_z0.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # Z/Z0 entry
        row += 1
        ttk.Label(self.fm_z, text='Z/Z0:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_z_z0 = ttk.Entry(self.fm_z, textvariable=self.field_z_z0, state='readonly', width=10)
        self.ent_z_z0.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # Z0/Z entry
        row += 1
        ttk.Label(self.fm_z, text='Z0/Z:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_z0_z = ttk.Entry(self.fm_z, textvariable=self.field_z0_z, state='readonly', width=10)
        self.ent_z0_z.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

        # correction frame
        self.fm_cor = ttk.LabelFrame(self, text='Correction')
        self.fm_cor.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_cor.columnconfigure(0, minsize=125)
        # C entry
        row = 0
        ttk.Label(self.fm_cor, text='Coefficient C:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_c = ttk.Entry(self.fm_cor, textvariable=self.field_c_coef, state='readonly', width=10)
        self.ent_c.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # corrected flow entry
        row += 1
        ttk.Label(self.fm_cor, text='Volume de base:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_c_flow = ttk.Entry(self.fm_cor, textvariable=self.field_vol_cor, state='readonly', width=10)
        self.ent_c_flow.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_cor, text='nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')

        # first SGERG compute to update results widgets with default gas composition
        self._run_sgerg()

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

    def _on_fields_update(self, *_args):
        self._run_sgerg()

    def _run_sgerg(self):
        try:
            # extract and format fields
            pcs = int(self.field_pcs.get())
            density = float(self.field_dens.get())
            x_co2 = float(self.field_co2.get()) / 100
            x_h2 = float(self.field_h2.get()) / 100
            press_bar = float(self.field_pres.get())
            temp_c = float(self.field_temp.get())
            temp_k = to_kelvin(temp_c)
            vol_raw = float(self.field_vol_raw.get())
            # french PCS k(wh/nm3, t_comb = 0 °C) to SGERG Hs (MJ/nm3, t_comb = 25 °C)
            hs_t25 = hs_to_t25(pcs/1000)
            hs_t25_mj = hs_to_mj(hs_t25)
            # do SGERG
            sgerg = SGERG(hs=hs_t25_mj, d=density, x_co2=x_co2, x_h2=x_h2)
            z, _ = sgerg.run(p_bar=press_bar, t_celsius=temp_c)
            z0, _ = sgerg.run(p_bar=PRES_REF, t_celsius=TEMP_REF_C)
            c_coef = press_bar/PRES_REF * TEMP_REF_K/temp_k * z0/z
            # update result fields
            self.field_z.set(f'{z:.04f}')
            self.field_z0.set(f'{z0:.04f}')
            self.field_z_z0.set(f'{z/z0:.04f}')
            self.field_z0_z.set(f'{z0/z:.04f}')
            self.field_c_coef.set(f'{c_coef:.04f}')
            self.field_vol_cor.set(f'{vol_raw * c_coef:_.0f}'.replace('_', ' '))
        except Exception:
            # mark fields as non-existent
            self.field_z.set('n/a')
            self.field_z0.set('n/a')
            self.field_z_z0.set('n/a')
            self.field_z0_z.set('n/a')
            self.field_c_coef.set('n/a')
            self.field_vol_cor.set('n/a')
            # debug
            if self.app_conf.debug:
                traceback.print_exc()

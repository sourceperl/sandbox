import tkinter as tk
import traceback
from tkinter import ttk

from aga8.AGA8 import AGA8Detail

from .conf import AppConf
from .const import PRES_REF, TEMP_REF_C, TEMP_REF_K
from .misc import to_kelvin

# some local const
INIT_DENSITY = 0.610
INIT_N2 = 1.68
INIT_CO2 = 0.69
INIT_CH4 = 90.95
INIT_C2H6 = 5.42
INIT_C3H8 = 0.98
INIT_NC4H10 = 0.05
INIT_IC4H10 = 0.05
INIT_NC5H12 = 0.08
INIT_IC5H12 = 0.09
INIT_IC5H12 = 0.09
INIT_NC6H14 = 0.01
INIT_C6H14 = 0.01
INIT_PRES = 60.0
INIT_TEMP = 16.85
INIT_RAW_VOL = 1000.0


class TabAGA8(tk.Frame):
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
        self.field_n2 = tk.StringVar(value=f'{INIT_N2:.2f}')
        self.field_n2.trace_add('write', self._on_fields_update)
        self.field_co2 = tk.StringVar(value=f'{INIT_CO2:.2f}')
        self.field_co2.trace_add('write', self._on_fields_update)
        self.field_ch4 = tk.StringVar(value=f'{INIT_CH4:.2f}')
        self.field_ch4.trace_add('write', self._on_fields_update)
        self.field_c2h6 = tk.StringVar(value=f'{INIT_C2H6:.2f}')
        self.field_c2h6.trace_add('write', self._on_fields_update)
        self.field_c3h8 = tk.StringVar(value=f'{INIT_C3H8:.2f}')
        self.field_c3h8.trace_add('write', self._on_fields_update)
        self.field_nc4h10 = tk.StringVar(value=f'{INIT_NC4H10:.2f}')
        self.field_nc4h10.trace_add('write', self._on_fields_update)
        self.field_ic4h10 = tk.StringVar(value=f'{INIT_IC4H10:.2f}')
        self.field_ic4h10.trace_add('write', self._on_fields_update)
        self.field_nc5h12 = tk.StringVar(value=f'{INIT_NC5H12:.2f}')
        self.field_nc5h12.trace_add('write', self._on_fields_update)
        self.field_ic5h12 = tk.StringVar(value=f'{INIT_IC5H12:.2f}')
        self.field_ic5h12.trace_add('write', self._on_fields_update)
        self.field_nc6h14 = tk.StringVar(value=f'{INIT_NC6H14:.2f}')
        self.field_nc6h14.trace_add('write', self._on_fields_update)
        self.field_pres = tk.StringVar(value=f'{INIT_PRES:.2f}')
        self.field_pres.trace_add('write', self._on_fields_update)
        self.field_temp = tk.StringVar(value=f'{INIT_TEMP:.2f}')
        self.field_temp.trace_add('write', self._on_fields_update)
        self.field_vol_raw = tk.StringVar(value=f'{INIT_RAW_VOL:.2f}')
        self.field_vol_raw.trace_add('write', self._on_fields_update)
        # variables to store ttk.Entry OUT values
        self.field_sum = tk.StringVar()
        self.field_z = tk.StringVar()
        self.field_z0 = tk.StringVar()
        self.field_z_z0 = tk.StringVar()
        self.field_z0_z = tk.StringVar()
        self.field_c_coef = tk.StringVar()
        self.field_vol_cor = tk.StringVar()

        # add ttk.Entry widget commands for validation
        # v_int_cmd = (self.register(self._valid_int), '%P')
        v_float_cmd = (self.register(self._valid_float), '%P')

        # create and place widgets
        # composition frame
        self.fm_comp = ttk.LabelFrame(self, text='Composition en fraction molaire')
        self.fm_comp.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_comp.columnconfigure(0, minsize=75)
        self.fm_comp.columnconfigure(2, minsize=40)
        self.fm_comp.columnconfigure(3, minsize=75)
        self.fm_comp.columnconfigure(5, minsize=40)
        # n2 entry
        row = 0
        ttk.Label(self.fm_comp, text='N2:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_h2 = ttk.Entry(self.fm_comp, textvariable=self.field_n2,
                                validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_h2.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # co2 entry
        row += 1
        ttk.Label(self.fm_comp, text='CO2:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_co2 = ttk.Entry(self.fm_comp, textvariable=self.field_co2,
                                 validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_co2.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # ch4 entry
        row += 1
        ttk.Label(self.fm_comp, text='CH4:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_ch4 = ttk.Entry(self.fm_comp, textvariable=self.field_ch4,
                                 validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_ch4.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # c2h6 entry
        row += 1
        ttk.Label(self.fm_comp, text='C2H6:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_c2h6 = ttk.Entry(self.fm_comp, textvariable=self.field_c2h6,
                                  validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_c2h6.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # c3h8 entry
        row += 1
        ttk.Label(self.fm_comp, text='C3H8:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_c3h8 = ttk.Entry(self.fm_comp, textvariable=self.field_c3h8,
                                  validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_c3h8.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # nc4h10 entry
        row = 0
        ttk.Label(self.fm_comp, text='NC4H10:').grid(row=row, column=3, padx=5, pady=5, sticky='w')
        self.ent_nc4h10 = ttk.Entry(self.fm_comp, textvariable=self.field_nc4h10,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_nc4h10.grid(row=row, column=4, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=5, padx=5, pady=5, sticky='w')
        # ic4h10 entry
        row += 1
        ttk.Label(self.fm_comp, text='IC4H10:').grid(row=row, column=3, padx=5, pady=5, sticky='w')
        self.ent_ic4h10 = ttk.Entry(self.fm_comp, textvariable=self.field_ic4h10,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_ic4h10.grid(row=row, column=4, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=5, padx=5, pady=5, sticky='w')
        # nc5h12 entry
        row += 1
        ttk.Label(self.fm_comp, text='NC5H12:').grid(row=row, column=3, padx=5, pady=5, sticky='w')
        self.ent_nc5h12 = ttk.Entry(self.fm_comp, textvariable=self.field_nc5h12,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_nc5h12.grid(row=row, column=4, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=5, padx=5, pady=5, sticky='w')
        # ic5h12 entry
        row += 1
        ttk.Label(self.fm_comp, text='IC5H12:').grid(row=row, column=3, padx=5, pady=5, sticky='w')
        self.ent_ic5h12 = ttk.Entry(self.fm_comp, textvariable=self.field_ic5h12,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_ic5h12.grid(row=row, column=4, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=5, padx=5, pady=5, sticky='w')
        # nc6h14 entry
        row += 1
        ttk.Label(self.fm_comp, text='NC6H14:').grid(row=row, column=3, padx=5, pady=5, sticky='w')
        self.ent_nc6h14 = ttk.Entry(self.fm_comp, textvariable=self.field_nc6h14,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_nc6h14.grid(row=row, column=4, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=5, padx=5, pady=5, sticky='w')
        # sum entry
        row += 1
        ttk.Label(self.fm_comp, text='Somme:').grid(row=row, column=3, padx=5, pady=5, sticky='w')
        self.ent_sum = ttk.Entry(self.fm_comp, textvariable=self.field_sum,
                                 validate='key', validatecommand=v_float_cmd, state='readonly', width=8)
        self.ent_sum.grid(row=row, column=4, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=5, padx=5, pady=5, sticky='w')

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
        ttk.Label(self.fm_met, text='Volume brut:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_vol = ttk.Entry(self.fm_met, textvariable=self.field_vol_raw,
                                 validate='key', validatecommand=v_float_cmd, width=10)
        self.ent_vol.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_met, text='m\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')

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

        # Z frame
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
        ttk.Label(self.fm_cor, text='Volume corrigé:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_c_flow = ttk.Entry(self.fm_cor, textvariable=self.field_vol_cor, state='readonly', width=10)
        self.ent_c_flow.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_cor, text='nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')

        # first AGA8 compute to update results widgets with default gas composition
        self._run_aga8()

    def _valid_int(self, new_value: str):
        if not new_value:
            return True
        for char in new_value:
            if char not in '+0123456789':
                return False
        return True

    def _valid_float(self, new_value: str):
        if not new_value:
            return True
        for char in new_value:
            if char not in '+-.0123456789':
                return False
        return True

    def _on_fields_update(self, *_args):
        self._run_aga8()

    def _run_aga8(self):
        try:
            # manage gas composition fields
            try:
                # extract and format
                x_ch4 = float(self.field_ch4.get())
                x_n2 = float(self.field_n2.get())
                x_co2 = float(self.field_co2.get())
                x_c2h6 = float(self.field_c2h6.get())
                x_c3h8 = float(self.field_c3h8.get())
                x_ic4h10 = float(self.field_ic4h10.get())
                x_nc4h10 = float(self.field_nc4h10.get())
                x_ic5h12 = float(self.field_ic5h12.get())
                x_nc5h12 = float(self.field_nc5h12.get())
                x_nc6h14 = float(self.field_nc6h14.get())
                # update sum
                x_sum = x_ch4 + x_n2 + x_co2 + x_c2h6 + x_c3h8
                x_sum += x_ic4h10 + x_nc4h10 + x_ic5h12 + x_nc5h12 + x_nc6h14
                self.field_sum.set(f'{x_sum:.02f}')
            except ValueError:
                # unable to compute sum
                self.field_sum.set('n/a')
                raise ValueError
            # manage gas counting fields
            press_bar = float(self.field_pres.get())
            temp_c = float(self.field_temp.get())
            temp_k = to_kelvin(temp_c)
            vol_raw = float(self.field_vol_raw.get())
            # do AGA8 (pass value as ratio 0.0 to 1.0)
            x = [
                0.0,             # 0 - PLACEHOLDER
                x_ch4 / 100,     # 1 - Methane C1 (CH4)
                x_n2 / 100,      # 2 - Nitrogen (N)
                x_co2 / 100,     # 3 - Carbon dioxide (CO2)
                x_c2h6 / 100,    # 4 - Ethane C2 (C2H6)
                x_c3h8 / 100,    # 5 - Propane C3 (C3H8)
                x_ic4h10 / 100,  # 6 - Iso-Butane IC4 (i-C4H10)
                x_nc4h10 / 100,  # 7 - n-Butane NC4 (n-C4H10)
                x_ic5h12 / 100,  # 8 - Isopentane IC5 (i-C5H12)
                x_nc5h12 / 100,  # 9 - n-Pentane NC5 (n-C5H12)
                x_nc6h14 / 100,  # 10 - n-Hexane (C6H14)
                0.0,             # 11 - n-Heptane (C7H16)
                0.0,             # 12 - n-Octane (C8H18)
                0.0,             # 13 - n-Nonane (C9H20)
                0.0,             # 14 - n-Decane (C10H22)
                0.0,             # 15 - Hydrogen (H)
                0.0,             # 16 - Oxygen (O)
                0.0,             # 17 - Carbon monoxide (CO)
                0.0,             # 18 - Water (H2O)
                0.0,             # 19 - Hydrogen sulfide (H2S)
                0.0,             # 20 - Helium (He)
                0.0,             # 21 - Argon (Ar)
            ]
            # use AGA8Detail class
            aga8_detail = AGA8Detail(p_bara=press_bar, t_celsius=temp_c, x=x).run()
            aga8_detail_ref = AGA8Detail(p_bara=PRES_REF, t_celsius=TEMP_REF_C, x=x).run()
            if aga8_detail.z is None or aga8_detail_ref.z is None:
                raise ValueError
            z = aga8_detail.z
            z0 = aga8_detail_ref.z
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

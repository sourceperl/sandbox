import tkinter as tk
import traceback
from tkinter import ttk

from ISO_6976 import ISO_6976

from .conf import AppConf
from .misc import set_grid_conf

# some local const
INIT_N2 = 1.68
INIT_O2 = 0.0
INIT_CO2 = 0.69
INIT_H2 = 0.0
INIT_CH4 = 90.95
INIT_C2H6 = 5.42
INIT_C3H8 = 0.98
INIT_N_C4H10 = 0.05
INIT_ISO_C4H10 = 0.05
INIT_N_C5H12 = 0.08
INIT_ISO_C5H12 = 0.09
INIT_NEO_C5H12 = 0.0
INIT_N_C6H14 = 0.01


class TabPCS(ttk.Frame):
    def __init__(self, master: tk.Tk, app_conf: AppConf, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        # global tk app shortcuts
        self.tk_app = master
        self.app_conf = app_conf

        # uniform geometry for this frame
        set_grid_conf(self)

        # variables to store ttk.Entry IN values (with write handlers)
        self.field_n2 = tk.StringVar(value=f'{INIT_N2:.3f}')
        self.field_n2.trace_add('write', self._on_fields_update)
        self.field_o2 = tk.StringVar(value=f'{INIT_O2:.3f}')
        self.field_o2.trace_add('write', self._on_fields_update)
        self.field_co2 = tk.StringVar(value=f'{INIT_CO2:.3f}')
        self.field_co2.trace_add('write', self._on_fields_update)
        self.field_h2 = tk.StringVar(value=f'{INIT_H2:.3f}')
        self.field_h2.trace_add('write', self._on_fields_update)
        self.field_ch4 = tk.StringVar(value=f'{INIT_CH4:.3f}')
        self.field_ch4.trace_add('write', self._on_fields_update)
        self.field_c2h6 = tk.StringVar(value=f'{INIT_C2H6:.3f}')
        self.field_c2h6.trace_add('write', self._on_fields_update)
        self.field_c3h8 = tk.StringVar(value=f'{INIT_C3H8:.3f}')
        self.field_c3h8.trace_add('write', self._on_fields_update)
        self.field_nc4h10 = tk.StringVar(value=f'{INIT_N_C4H10:.3f}')
        self.field_nc4h10.trace_add('write', self._on_fields_update)
        self.field_iso_c4h10 = tk.StringVar(value=f'{INIT_ISO_C4H10:.3f}')
        self.field_iso_c4h10.trace_add('write', self._on_fields_update)
        self.field_n_c5h12 = tk.StringVar(value=f'{INIT_N_C5H12:.3f}')
        self.field_n_c5h12.trace_add('write', self._on_fields_update)
        self.field_iso_c5h12 = tk.StringVar(value=f'{INIT_ISO_C5H12:.3f}')
        self.field_iso_c5h12.trace_add('write', self._on_fields_update)
        self.field_neo_c5h12 = tk.StringVar(value=f'{INIT_NEO_C5H12:.3f}')
        self.field_neo_c5h12.trace_add('write', self._on_fields_update)
        self.field_n_c6h14 = tk.StringVar(value=f'{INIT_N_C6H14:.3f}')
        self.field_n_c6h14.trace_add('write', self._on_fields_update)
        # variables to store ttk.Entry OUT values
        self.field_sum = tk.StringVar()
        self.field_zo_t0_0 = tk.StringVar()
        self.field_pcs_t0_0 = tk.StringVar()
        self.field_pci_t0_0 = tk.StringVar()
        self.field_density_t0_0 = tk.StringVar()
        self.field_rel_density_t0_0 = tk.StringVar()
        self.field_wobbe_t0_0 = tk.StringVar()
        self.field_pcs_t25_0 = tk.StringVar()
        self.field_pci_t25_0 = tk.StringVar()
        self.field_wobbe_t25_0 = tk.StringVar()
        self.field_pcs_t15_15 = tk.StringVar()
        self.field_pci_t15_15 = tk.StringVar()
        self.field_wobbe_t15_15 = tk.StringVar()

        # add ttk.Entry widget commands for validation
        # v_int_cmd = (self.register(self._valid_int), '%P', '%W')
        v_float_cmd = (self.register(self._valid_float), '%P', '%W')

        # create and place widgets
        # composition frame
        self.fm_comp = ttk.LabelFrame(self, text='Composition en fraction molaire')
        self.fm_comp.grid(row=0, rowspan=2, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_comp.columnconfigure(0, minsize=175)
        self.fm_comp.columnconfigure(2, minsize=40)
        # Nitrogen (N2) entry
        row = 0
        ttk.Label(self.fm_comp, text='Azote (N2):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_n2, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Oxygen (O2) entry
        row += 1
        ttk.Label(self.fm_comp, text='Oxygène (O2):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_o2, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Carbon dioxide (CO2) entry
        row += 1
        ttk.Label(self.fm_comp, text='Dioxyde de carbonne (CO2):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_co2, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Hydrogen (H2) entry
        row += 1
        ttk.Label(self.fm_comp, text='Hydrogène (H2):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_h2, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Methane (CH4) entry
        row += 1
        ttk.Label(self.fm_comp, text='Methane (CH4):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_ch4, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Ethane (C2H6) entry
        row += 1
        ttk.Label(self.fm_comp, text='Ethane (C2H6):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_c2h6, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Propane (C3H8) entry
        row += 1
        ttk.Label(self.fm_comp, text='Propane (C3H8):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_c3h8, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # n-Butane (n-C4H10) entry
        row += 1
        ttk.Label(self.fm_comp, text='n-Butane (n-C4H10):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_nc4h10, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Isobutane (2-Methylpropane i-C4H10) entry
        row += 1
        ttk.Label(self.fm_comp, text='Isobutane (i-C4H10):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_iso_c4h10, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # n-Pentane (n-c5h12) entry
        row += 1
        ttk.Label(self.fm_comp, text='n-Pentane (n-C5H12):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_n_c5h12, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Isopentane (2-Methylbutane i-C5H12) entry
        row += 1
        ttk.Label(self.fm_comp, text='Isopentane (i-C5H12):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_iso_c5h12, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Neopentane (2,2-Dimethylpropane neo-C5H12) entry
        row += 1
        ttk.Label(self.fm_comp, text='Neopentane (neo-C5H12):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_neo_c5h12, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # n-Hexane (n-C6H14) entry
        row += 1
        ttk.Label(self.fm_comp, text='n-Hexane (n-C6H14):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_n_c6h14, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # sum entry
        row += 1
        ttk.Label(self.fm_comp, text='Somme des constituants:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_comp, textvariable=self.field_sum, state='readonly',
                  width=8).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')

        # result 0°C/0°C frame
        self.fm_res_t0_0 = ttk.LabelFrame(self, text='Résultats 0/0')
        self.fm_res_t0_0.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_res_t0_0.columnconfigure(0, minsize=140)
        # PCS entry
        row = 0
        ttk.Label(self.fm_res_t0_0, text='PCS:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_t0_0, textvariable=self.field_pcs_t0_0, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_t0_0, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # PCI entry
        row += 1
        ttk.Label(self.fm_res_t0_0, text='PCI:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_t0_0, textvariable=self.field_pci_t0_0, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_t0_0, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # wobbe entry
        row += 1
        ttk.Label(self.fm_res_t0_0, text='Wobbe:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_t0_0, textvariable=self.field_wobbe_t0_0, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_t0_0, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # density entry
        row += 1
        ttk.Label(self.fm_res_t0_0, text='Masse volumique:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_t0_0, textvariable=self.field_density_t0_0, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_t0_0, text='kg/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # relative density entry
        row += 1
        ttk.Label(self.fm_res_t0_0, text='Densité relative:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_t0_0, textvariable=self.field_rel_density_t0_0, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # Z0 entry
        row += 1
        ttk.Label(self.fm_res_t0_0, text='Z0:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_t0_0, textvariable=self.field_zo_t0_0, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')

        # result 25°C/0°C frame
        self.fm_res_others = ttk.LabelFrame(self, text='Autres résultats')
        self.fm_res_others.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_res_others.columnconfigure(0, minsize=140)
        # PCS entry
        row = 0
        ttk.Label(self.fm_res_others, text='PCS (25/0):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_others, textvariable=self.field_pcs_t25_0, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_others, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # PCI entry
        row += 1
        ttk.Label(self.fm_res_others, text='PCI (25/0):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_others, textvariable=self.field_pci_t25_0, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_others, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # wobbe entry
        row += 1
        ttk.Label(self.fm_res_others, text='Wobbe (25/0):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_others, textvariable=self.field_wobbe_t25_0, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_others, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # PCS entry
        row += 1
        ttk.Label(self.fm_res_others, text='PCS (15/15):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_others, textvariable=self.field_pcs_t15_15, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_others, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # PCI entry
        row += 1
        ttk.Label(self.fm_res_others, text='PCI (15/15):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_others, textvariable=self.field_pci_t15_15, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_others, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # wobbe entry
        row += 1
        ttk.Label(self.fm_res_others, text='Wobbe (15/15):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(self.fm_res_others, textvariable=self.field_wobbe_t15_15, state='readonly',
                  width=10).grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_res_others, text='Wh/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')

        # first compute to update results widgets with default gas composition
        self._compute()

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
        self._compute()

    def _compute(self):
        try:
            # manage gas composition fields
            try:
                # extract and format
                iso_6976 = ISO_6976(x_as_ratio=False,
                                    x_n2=float(self.field_n2.get()),
                                    x_o2=float(self.field_o2.get()),
                                    x_co2=float(self.field_co2.get()),
                                    x_h2=float(self.field_h2.get()),
                                    x_ch4=float(self.field_ch4.get()),
                                    x_c2h6=float(self.field_c2h6.get()),
                                    x_c3h8=float(self.field_c3h8.get()),
                                    x_iso_c4h10=float(self.field_iso_c4h10.get()),
                                    x_n_c4h10=float(self.field_nc4h10.get()),
                                    x_iso_c5h12=float(self.field_iso_c5h12.get()),
                                    x_n_c5h12=float(self.field_n_c5h12.get()),
                                    x_neo_c5h12=float(self.field_neo_c5h12.get()),
                                    x_n_c6h14=float(self.field_n_c6h14.get()),
                                    )
                self.field_sum.set(f'{iso_6976.x_sum:.02f}')
            except ValueError:
                # unable to compute sum
                self.field_sum.set('n/a')
                raise ValueError
            # update result fields
            # 0°C/0°C
            iso_6976.t_combustion = 0
            iso_6976.t_metering = 0
            self.field_zo_t0_0.set(f'{iso_6976.z0:.04f}')
            self.field_pcs_t0_0.set(f'{iso_6976.hhv_wh:.0f}')
            self.field_pci_t0_0.set(f'{iso_6976.lhv_wh:.0f}')
            self.field_density_t0_0.set(f'{iso_6976.density:.4f}')
            self.field_rel_density_t0_0.set(f'{iso_6976.rel_density:.3f}')
            self.field_wobbe_t0_0.set(f'{iso_6976.wobbe_wh:.0f}')
            # 25°C/0°C
            iso_6976.t_combustion = 25
            iso_6976.t_metering = 0
            self.field_pcs_t25_0.set(f'{iso_6976.hhv_wh:.0f}')
            self.field_pci_t25_0.set(f'{iso_6976.lhv_wh:.0f}')
            self.field_wobbe_t25_0.set(f'{iso_6976.wobbe_wh:.0f}')
            # 15°C/15°C
            iso_6976.t_combustion = 15
            iso_6976.t_metering = 15
            self.field_pcs_t15_15.set(f'{iso_6976.hhv_wh:.0f}')
            self.field_pci_t15_15.set(f'{iso_6976.lhv_wh:.0f}')
            self.field_wobbe_t15_15.set(f'{iso_6976.wobbe_wh:.0f}')
        except Exception:
            # mark fields as non-existent
            self.field_zo_t0_0.set('n/a')
            self.field_pcs_t0_0.set('n/a')
            self.field_pci_t0_0.set('n/a')
            self.field_density_t0_0.set('n/a')
            self.field_rel_density_t0_0.set('n/a')
            self.field_wobbe_t0_0.set('n/a')
            self.field_pcs_t25_0.set('n/a')
            self.field_pci_t25_0.set('n/a')
            self.field_wobbe_t25_0.set('n/a')
            self.field_pcs_t15_15.set('n/a')
            self.field_pci_t15_15.set('n/a')
            self.field_wobbe_t15_15.set('n/a')
            # debug
            if self.app_conf.debug:
                traceback.print_exc()

import tkinter as tk
import traceback
from math import sqrt
from tkinter import ttk

from .conf import AppConf

# some local const
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


INIT_N2 = 0.299
INIT_CO2 = 0.0
INIT_CH4 = 93.955
INIT_C2H6 = 4.929
INIT_C3H8 = 0.483
INIT_NC4H10 = 0.0
INIT_IC4H10 = 0.151
INIT_NC5H12 = 0.177
INIT_IC5H12 = 0.005
INIT_NC6H14 = 0.00


class TabPCS(ttk.Frame):
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
        self.field_n2 = tk.StringVar(value=f'{INIT_N2:.3f}')
        self.field_n2.trace_add('write', self._on_fields_update)
        self.field_co2 = tk.StringVar(value=f'{INIT_CO2:.3f}')
        self.field_co2.trace_add('write', self._on_fields_update)
        self.field_ch4 = tk.StringVar(value=f'{INIT_CH4:.3f}')
        self.field_ch4.trace_add('write', self._on_fields_update)
        self.field_c2h6 = tk.StringVar(value=f'{INIT_C2H6:.3f}')
        self.field_c2h6.trace_add('write', self._on_fields_update)
        self.field_c3h8 = tk.StringVar(value=f'{INIT_C3H8:.3f}')
        self.field_c3h8.trace_add('write', self._on_fields_update)
        self.field_nc4h10 = tk.StringVar(value=f'{INIT_NC4H10:.3f}')
        self.field_nc4h10.trace_add('write', self._on_fields_update)
        self.field_ic4h10 = tk.StringVar(value=f'{INIT_IC4H10:.3f}')
        self.field_ic4h10.trace_add('write', self._on_fields_update)
        self.field_nc5h12 = tk.StringVar(value=f'{INIT_NC5H12:.3f}')
        self.field_nc5h12.trace_add('write', self._on_fields_update)
        self.field_ic5h12 = tk.StringVar(value=f'{INIT_IC5H12:.3f}')
        self.field_ic5h12.trace_add('write', self._on_fields_update)
        self.field_nc6h14 = tk.StringVar(value=f'{INIT_NC6H14:.3f}')
        self.field_nc6h14.trace_add('write', self._on_fields_update)
        # variables to store ttk.Entry OUT values
        self.field_sum = tk.StringVar()
        self.field_zo = tk.StringVar()
        self.field_pcs = tk.StringVar()
        self.field_pci = tk.StringVar()
        self.field_density = tk.StringVar()
        self.field_rel_density = tk.StringVar()
        self.field_wobbe = tk.StringVar()

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
        self.ent_h2 = ttk.Entry(self.fm_comp, textvariable=self.field_n2,
                                validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_h2.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Carbon dioxide (CO2) entry
        row += 1
        ttk.Label(self.fm_comp, text='Dioxyde de carbonne (CO2):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_co2 = ttk.Entry(self.fm_comp, textvariable=self.field_co2,
                                 validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_co2.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Methane (CH4) entry
        row += 1
        ttk.Label(self.fm_comp, text='Methane (CH4):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_ch4 = ttk.Entry(self.fm_comp, textvariable=self.field_ch4,
                                 validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_ch4.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Ethane (C2H6) entry
        row += 1
        ttk.Label(self.fm_comp, text='Ethane (C2H6):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_c2h6 = ttk.Entry(self.fm_comp, textvariable=self.field_c2h6,
                                  validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_c2h6.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Propane (C3H8) entry
        row += 1
        ttk.Label(self.fm_comp, text='Propane (C3H8):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_c3h8 = ttk.Entry(self.fm_comp, textvariable=self.field_c3h8,
                                  validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_c3h8.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # n-Butane (n-C4H10) entry
        row += 1
        ttk.Label(self.fm_comp, text='n-Butane (n-C4H10):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_nc4h10 = ttk.Entry(self.fm_comp, textvariable=self.field_nc4h10,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_nc4h10.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Isobutane (2-Methylpropane i-C4H10) entry
        row += 1
        ttk.Label(self.fm_comp, text='Isobutane(i-C4H10):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_ic4h10 = ttk.Entry(self.fm_comp, textvariable=self.field_ic4h10,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_ic4h10.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # n-Pentane (n-c5h12) entry
        row += 1
        ttk.Label(self.fm_comp, text='n-Pentane (n-C5H12):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_nc5h12 = ttk.Entry(self.fm_comp, textvariable=self.field_nc5h12,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_nc5h12.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # Isopentane (2-Methylbutane i-C5H12) entry
        row += 1
        ttk.Label(self.fm_comp, text='Isopentane (i-C5H12):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_ic5h12 = ttk.Entry(self.fm_comp, textvariable=self.field_ic5h12,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_ic5h12.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # n-Hexane (n-C6H14) entry
        row += 1
        ttk.Label(self.fm_comp, text='n-Hexane (n-C6H14):').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_nc6h14 = ttk.Entry(self.fm_comp, textvariable=self.field_nc6h14,
                                    validate='key', validatecommand=v_float_cmd, width=8)
        self.ent_nc6h14.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        # sum entry
        row += 1
        ttk.Label(self.fm_comp, text='Somme:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_sum = ttk.Entry(self.fm_comp, textvariable=self.field_sum,
                                 validate='key', validatecommand=v_float_cmd, state='readonly', width=8)
        self.ent_sum.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(self.fm_comp, text='%').grid(row=row, column=2, padx=5, pady=5, sticky='w')

        # compressibility factor frame
        self.fm_res = ttk.LabelFrame(self, text='Résultats (à 0°C)')
        self.fm_res.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
        self.fm_res.columnconfigure(0, minsize=125)
        # PCS entry
        row = 0
        ttk.Label(self.fm_res, text='PCS:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_pcs = ttk.Entry(self.fm_res, textvariable=self.field_pcs, state='readonly', width=10)
        self.ent_pcs.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # PCI entry
        row += 1
        ttk.Label(self.fm_res, text='PCI:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_pcs = ttk.Entry(self.fm_res, textvariable=self.field_pci, state='readonly', width=10)
        self.ent_pcs.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # wobbe entry
        row += 1
        ttk.Label(self.fm_res, text='Wobbe:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_pcs = ttk.Entry(self.fm_res, textvariable=self.field_wobbe, state='readonly', width=10)
        self.ent_pcs.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # density entry
        row += 1
        ttk.Label(self.fm_res, text='Masse volumique:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_pcs = ttk.Entry(self.fm_res, textvariable=self.field_density, state='readonly', width=10)
        self.ent_pcs.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # relative density entry
        row += 1
        ttk.Label(self.fm_res, text='Densité relative:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_pcs = ttk.Entry(self.fm_res, textvariable=self.field_rel_density, state='readonly', width=10)
        self.ent_pcs.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        # Z0 entry
        row += 1
        ttk.Label(self.fm_res, text='Z0:').grid(row=row, column=0, padx=5, pady=5, sticky='w')
        self.ent_pcs = ttk.Entry(self.fm_res, textvariable=self.field_zo, state='readonly', width=10)
        self.ent_pcs.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

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
                x_n2 = float(self.field_n2.get())
                x_co2 = float(self.field_co2.get())
                x_ch4 = float(self.field_ch4.get())
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
            # compute Z0: apply weights to every components
            z_sum = 0.022_4 * x_n2
            z_sum += 0.081_9 * x_co2
            z_sum += 0.049_0 * x_ch4
            z_sum += 0.100_0 * x_c2h6
            z_sum += 0.145_3 * x_c3h8
            z_sum += 0.206_9 * x_nc4h10
            z_sum += 0.204_9 * x_ic4h10
            z_sum += 0.286_4 * x_nc5h12
            z_sum += 0.251_0 * x_ic5h12
            z_sum += 0.328_6 * x_nc6h14
            z0 = 1 - (z_sum/100)**2
            # compute PCS
            pcs_kj = 0 * x_n2 / 100
            pcs_kj += 0 * x_co2 / 100
            pcs_kj += 39_840 * x_ch4 / 100
            pcs_kj += 69_790 * x_c2h6 / 100
            pcs_kj += 99_220 * x_c3h8 / 100
            pcs_kj += 128_660 * x_nc4h10 / 100
            pcs_kj += 128_230 * x_ic4h10 / 100
            pcs_kj += 158_070 * x_nc5h12 / 100
            pcs_kj += 157_760 * x_ic5h12 / 100
            pcs_kj += 187_530 * x_nc6h14 / 100
            pcs_kj /= z0
            pcs_wh = pcs_kj / 3.6
            # compute PCI
            pci_kj = 0 * x_n2 / 100
            pci_kj += 0 * x_co2 / 100
            pci_kj += 35_818 * x_ch4 / 100
            pci_kj += 63_760 * x_c2h6 / 100
            pci_kj += 91_180 * x_c3h8 / 100
            pci_kj += 118_610 * x_nc4h10 / 100
            pci_kj += 118_180 * x_ic4h10 / 100
            pci_kj += 146_000 * x_nc5h12 / 100
            pci_kj += 145_690 * x_ic5h12 / 100
            pci_kj += 173_450 * x_nc6h14 / 100
            pci_kj /= z0
            pci_wh = pci_kj / 3.6
            # compute density
            rel_density_sum = 0.967_2 * x_n2 / 100
            rel_density_sum += 1.519_5 * x_co2 / 100
            rel_density_sum += 0.553_9 * x_ch4 / 100
            rel_density_sum += 1.038_2 * x_c2h6 / 100
            rel_density_sum += 1.522_4 * x_c3h8 / 100
            rel_density_sum += 2.006_7 * x_nc4h10 / 100
            rel_density_sum += 2.006_7 * x_ic4h10 / 100
            rel_density_sum += 2.491 * x_nc5h12 / 100
            rel_density_sum += 2.491 * x_ic5h12 / 100
            rel_density_sum += 3.891 * x_nc6h14 / 100
            rel_density_sum /= z0
            rel_density = 0.999_41 * rel_density_sum
            # compute wobbe
            wobbe = pcs_wh/sqrt(rel_density)
            # update result fields
            self.field_zo.set(f'{z0:.04f}')
            self.field_pcs.set(f'{pcs_wh:.0f}')
            self.field_pci.set(f'{pci_wh:.0f}')
            self.field_rel_density.set(f'{rel_density:.3f}')
            self.field_wobbe.set(f'{wobbe:.0f}')
        except Exception:
            # mark fields as non-existent
            self.field_pcs.set('n/a')
            self.field_pci.set('n/a')
            self.field_rel_density.set('n/a')
            self.field_wobbe.set('n/a')
            # debug
            if self.app_conf.debug:
                traceback.print_exc()

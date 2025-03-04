import tkinter as tk
from tkinter import ttk

from GERG_WATER import get_dew_point_c, get_vol_humidity

from .conf import AppConf
from .misc import TabTemplate

# some local const
INIT_PRES = 68.7
INIT_BASE_D = 0.7882
INIT_HUM = 40.0
INIT_DEW_POINT = -10.0


class TabWater(TabTemplate):
    def __init__(self, master: tk.Tk, app_conf: AppConf, *args, **kwargs) -> None:
        super().__init__(master, app_conf, *args, **kwargs)

        # variables to store ttk.Entry IN values (with write handlers)
        self.unit_mode_var = tk.StringVar(value='mg')
        self.unit_mode_var.trace_add('write', self._on_mode_change)
        self.unit_var = tk.StringVar()
        self.field_p_bara = tk.StringVar(value=f'{INIT_PRES:.1f}')
        self.field_p_bara.trace_add('write', self._on_humdity_change)
        self.field_p_bara.trace_add('write', self._on_dew_point_change)
        self.field_dens = tk.StringVar(value=f'{INIT_BASE_D:.3f}')
        self.field_dens.trace_add('write', self._on_humdity_change)
        self.field_dens.trace_add('write', self._on_dew_point_change)
        self.field_hum = tk.StringVar(value=f'{INIT_HUM:.1f}')
        self.field_hum.trace_add('write', self._on_humdity_change)
        self.field_dp = tk.StringVar(value=f'{INIT_DEW_POINT:.1f}')
        self.field_dp.trace_add('write', self._on_dew_point_change)
        # variables to store ttk.Entry OUT values (results)
        self.hum_conv_res_var = tk.StringVar()
        self.dp_conv_res_var = tk.StringVar()

        # add ttk.Entry widget commands for validation
        # v_int_cmd = (self.register(self._valid_int), '%P', '%W')
        v_float_cmd = (self.register(self._valid_float), '%P', '%W')

        # create and place widgets
        self.center_f = ttk.Frame(self)
        self.center_f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # mode ppmv/mg
        row = 0
        ttk.Label(self.center_f, text='Mode:').grid(row=row, column=2, padx=5, pady=5, sticky='e')
        ttk.Radiobutton(self.center_f, text='mg/nm\u00b3', value='mg',
                        variable=self.unit_mode_var).grid(row=row, column=3, padx=5, pady=5, sticky='w')
        ttk.Radiobutton(self.center_f, text='ppmv', value='ppmv',
                        variable=self.unit_mode_var).grid(row=row, column=4, padx=5, pady=5, sticky='w')
        # pressure
        row += 1
        ttk.Label(self.center_f, text='Pression:').grid(row=row, column=2, padx=5, pady=5, sticky='e')
        ttk.Entry(self.center_f, textvariable=self.field_p_bara, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=3, padx=5, pady=5)
        ttk.Label(self.center_f, text='bara').grid(row=row, column=4, padx=5, pady=5, sticky='w')
        # density
        row += 1
        ttk.Label(self.center_f, text='Masse volumique:').grid(row=row, column=2, padx=5, pady=5, sticky='e')
        self.ent_density = ttk.Entry(self.center_f, textvariable=self.field_dens, validate='key',
                                     validatecommand=v_float_cmd, width=8)
        self.ent_density.grid(row=row, column=3, padx=5, pady=5)
        ttk.Label(self.center_f, text='kg/nm3').grid(row=row, column=4, padx=5, pady=5, sticky='w')
        # vertical space
        row += 1
        ttk.Label(self.center_f).grid(row=row, padx=5, pady=5)
        # absolut humidity -> dew point
        row += 1
        ttk.Label(self.center_f, text='Teneur en eau:').grid(row=row, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.center_f, textvariable=self.field_hum, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5)
        ttk.Label(self.center_f, textvariable=self.unit_var,
                  width=8).grid(row=row, column=2, padx=5, pady=5, sticky='w')
        ttk.Label(self.center_f, text='\u2794').grid(row=row, column=3, padx=20, pady=20)
        ttk.Label(self.center_f, text='Point de rosée:').grid(row=row, column=4, padx=5, pady=5)
        ttk.Entry(self.center_f, textvariable=self.hum_conv_res_var, state='readonly',
                  width=8).grid(row=row, column=5, padx=5, pady=5)
        ttk.Label(self.center_f, text='°C').grid(row=row, column=6, padx=5, pady=5, sticky='w')
        # vertical space
        row += 1
        ttk.Label(self.center_f).grid(row=row, padx=5, pady=5)
        # absolut dew point -> humidity
        row += 1
        ttk.Label(self.center_f, text='Point de rosée:').grid(row=row, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.center_f, textvariable=self.field_dp, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5)
        ttk.Label(self.center_f, text='°C').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        ttk.Label(self.center_f, text='\u2794').grid(row=row, column=3, padx=20, pady=20)
        ttk.Label(self.center_f, text='Teneur en eau:').grid(row=row, column=4, padx=5, pady=5)
        ttk.Entry(self.center_f, textvariable=self.dp_conv_res_var, state='readonly',
                  width=8).grid(row=row, column=5, padx=5, pady=5)
        ttk.Label(self.center_f, textvariable=self.unit_var,
                  width=6).grid(row=row, column=6, padx=5, pady=5, sticky='w')

        # init response fields
        self._on_mode_change()
        self._on_humdity_change()
        self._on_dew_point_change()

    def _on_mode_change(self, *_args):
        # customize widgets for current mode
        if self.unit_mode_var.get() == 'ppmv':
            self.ent_density.configure(state='normal')
            self.unit_var.set('ppmv')
        elif self.unit_mode_var.get() == 'mg':
            self.ent_density.configure(state='readonly')
            self.unit_var.set('mg/nm\u00b3')
        # update result fields
        self._on_humdity_change()
        self._on_dew_point_change()

    def _on_humdity_change(self, *_args):
        try:
            # common part
            p_bara = float(self.field_p_bara.get())
            # fill dew point result field
            if self.unit_mode_var.get() == 'mg':
                mg_nm3 = float(self.field_hum.get())
                dew_p = get_dew_point_c(vol_hum_mg=mg_nm3, p_bara=p_bara)
                self.hum_conv_res_var.set(f'{dew_p:.1f}')
            elif self.unit_mode_var.get() == 'ppmv':
                ppmv = float(self.field_hum.get())
                density = float(self.field_dens.get())
                dew_p = get_dew_point_c(vol_hum_mg=ppmv * density, p_bara=p_bara)
                self.hum_conv_res_var.set(f'{dew_p:.1f}')
        except ValueError:
            self.hum_conv_res_var.set('n/a')

    def _on_dew_point_change(self, *_args):
        try:
            # common part
            p_bara = float(self.field_p_bara.get())
            dew_point_c = float(self.field_dp.get())
            mg_nm3 = get_vol_humidity(dew_point_c=dew_point_c, p_bara=p_bara)
            # fill result field with currently selected unit
            if self.unit_mode_var.get() == 'mg':
                self.dp_conv_res_var.set(f'{mg_nm3:.1f}')
            elif self.unit_mode_var.get() == 'ppmv':
                density = float(self.field_dens.get())
                ppmv = mg_nm3/density
                self.dp_conv_res_var.set(f'{ppmv:.4f}')
        except (ValueError, ZeroDivisionError):
            self.dp_conv_res_var.set('n/a')

import tkinter as tk
from tkinter import ttk

from GERG_WATER import get_dew_point_c, get_vol_humidity

from .conf import AppConf
from .misc import TabTemplate

# some local const
INIT_PRES = 68.7
INIT_HUM = 40.0
INIT_DEW_POINT = -10.0


class TabWater(TabTemplate):
    def __init__(self, master: tk.Tk, app_conf: AppConf, *args, **kwargs) -> None:
        super().__init__(master, app_conf, *args, **kwargs)

        # variables to store ttk.Entry IN values (with write handlers)
        self.field_p_bara = tk.StringVar(value=f'{INIT_PRES:.1f}')
        self.field_p_bara.trace_add('write', self._on_humdity_change)
        self.field_p_bara.trace_add('write', self._on_dew_point_change)
        self.field_hum = tk.StringVar(value=f'{INIT_HUM:.1f}')
        self.field_hum.trace_add('write', self._on_humdity_change)
        self.field_dp = tk.StringVar(value=f'{INIT_DEW_POINT:.1f}')
        self.field_dp.trace_add('write', self._on_dew_point_change)
        # variables to store ttk.Entry OUT values
        self.field_r_dp = tk.StringVar()
        self.field_r_hum = tk.StringVar()

        # add ttk.Entry widget commands for validation
        # v_int_cmd = (self.register(self._valid_int), '%P', '%W')
        v_float_cmd = (self.register(self._valid_float), '%P', '%W')

        # create and place widgets
        self.center_f = ttk.Frame(self)
        self.center_f.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # pressure
        row = 0
        ttk.Label(self.center_f, text='Pression:').grid(row=row, column=2, padx=5, pady=5, sticky='e')
        ttk.Entry(self.center_f, textvariable=self.field_p_bara, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=3, padx=5, pady=5)
        ttk.Label(self.center_f, text='bara').grid(row=row, column=4, padx=5, pady=5, sticky='w')
        # vertical space
        row += 1
        ttk.Label(self.center_f).grid(row=row, padx=5, pady=5)
        # absolut humidity -> dew point
        row += 1
        ttk.Label(self.center_f, text='Teneur en eau:').grid(row=row, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.center_f, textvariable=self.field_hum, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5)
        ttk.Label(self.center_f, text='mg/nm\u00b3').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        ttk.Label(self.center_f, text='\u2794').grid(row=row, column=3, padx=20, pady=20)
        ttk.Label(self.center_f, text='Point de rosée:').grid(row=row, column=4, padx=5, pady=5)
        ttk.Entry(self.center_f, textvariable=self.field_r_dp, state='readonly',
                  width=8).grid(row=row, column=5, padx=5, pady=5)
        ttk.Label(self.center_f, text='°C').grid(row=row, column=6, padx=5, pady=5, sticky='w')
        # absolut dew point -> humidity
        row += 1
        ttk.Label(self.center_f, text='Point de rosée:').grid(row=row, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(self.center_f, textvariable=self.field_dp, validate='key', validatecommand=v_float_cmd,
                  width=8).grid(row=row, column=1, padx=5, pady=5)
        ttk.Label(self.center_f, text='°C').grid(row=row, column=2, padx=5, pady=5, sticky='w')
        ttk.Label(self.center_f, text='\u2794').grid(row=row, column=3, padx=20, pady=20)
        ttk.Label(self.center_f, text='Teneur en eau:').grid(row=row, column=4, padx=5, pady=5)
        ttk.Entry(self.center_f, textvariable=self.field_r_hum, state='readonly',
                  width=8).grid(row=row, column=5, padx=5, pady=5)
        ttk.Label(self.center_f, text='mg/nm\u00b3').grid(row=row, column=6, padx=5, pady=5, sticky='w')

        # init response fields
        self._on_humdity_change()
        self._on_dew_point_change()

    def _on_humdity_change(self, *_args):
        try:
            p_bara = float(self.field_p_bara.get())
            abs_hum = float(self.field_hum.get())
            self.field_r_dp.set(f'{get_dew_point_c(vol_hum_mg=abs_hum, p_bara=p_bara):.1f}')
        except ValueError:
            self.field_r_dp.set('n/a')

    def _on_dew_point_change(self, *_args):
        try:
            p_bara = float(self.field_p_bara.get())
            dew_point_c = float(self.field_dp.get())
            self.field_r_hum.set(f'{get_vol_humidity(dew_point_c=dew_point_c, p_bara=p_bara):.1f}')
        except ValueError:
            self.field_r_hum.set('n/a')

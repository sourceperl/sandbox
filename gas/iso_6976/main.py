from ISO_6976 import ISO_6976

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


iso_6976 = ISO_6976(t_combustion=0,
                    t_metering=0,
                    x_as_ratio=False,
                    x_n2=INIT_N2,
                    x_o2=INIT_O2,
                    x_co2=INIT_CO2,
                    x_h2=INIT_H2,
                    x_ch4=INIT_CH4,
                    x_c2h6=INIT_C2H6,
                    x_c3h8=INIT_C3H8,
                    x_iso_c4h10=INIT_ISO_C4H10,
                    x_n_c4h10=INIT_N_C4H10,
                    x_iso_c5h12=INIT_ISO_C5H12,
                    x_n_c5h12=INIT_N_C5H12,
                    x_neo_c5h12=INIT_NEO_C5H12,
                    x_n_c6h14=INIT_N_C6H14,
                    )

print(f'{iso_6976.z0=}')
print(f'{iso_6976.hhv_wh=}')
print(f'{iso_6976.lhv_wh=}')
print(f'{iso_6976.density=}')
print(f'{iso_6976.rel_density=}')
print(f'{iso_6976.wobbe_wh=}')

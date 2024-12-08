from SGERG_88 import SGERG

sgerg = SGERG(hs=40.66, d=0.581, x_co2=0.006, x_h2=0.0)
z, rho_m = sgerg.run(p_bar=60, t_celsius=-3.15)
print(f'z={z}, rho_m={rho_m}')

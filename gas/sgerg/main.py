from SGERG_88 import SGERG


sgerg= SGERG(hs=40.66, d=0.581, x_co2=0.006, x_h2=0.0)
print(sgerg.run(p_bar=60, t_c=-3.15))

""" Compute compression factor Z and molar density rho_m with SGERG method. """

from SGERG_88 import SGERG


# some functions
def hs_to_mj(hs_kwh: float) -> float:
    """Convert Hs from kwh/nm3 to MJ/nm3."""
    return hs_kwh * 3.6


def hs_to_t25(hs_t0: float) -> float:
    """Convert Hs from t_comb = 0°C to 25 °C."""
    return hs_t0 * 0.997_4


# convert Hs from 11.324 kwh/m3 at French conditions: kwh/nm3, t_comb = 0 °C, t ref metering = 0 °C and p = 1 ATM
# to SGERG conditions: MJ/nm3, t_comb = 25 °C, t_ref = 0 °C and p = 1 ATM (1.013_25 bar)
hs_t25 = hs_to_t25(11.324)
hs_t25_mj = hs_to_mj(hs_t25)

# init SGERG with the following gas quality :
#   calorific value = 40.66 MJ/m3 (sgerg conditions: t_comb = 25 °C, t_ref = 0 °C and p = 1 ATM (1.013_25 bar)
#   relative density = 0.581 (t_ref = 0 °C and p = 1 ATM (1.013_25 bar))
#   CO2 mole fraction = 0.006
#   H2 mole fraction = 0.0
sgerg = SGERG(hs=hs_t25_mj, d=0.581, x_co2=0.006, x_h2=0.0)

# get z and rho_m at 60 bara and -3.15 °C
z, rho_m = sgerg.run(p_bar=60, t_celsius=-3.15)
print(f'at 60 bara and -3.15 °C: z={z}, rho_m={rho_m}')

# get z and rho_m at 120 bara and -3.15 °C
z, rho_m = sgerg.run(p_bar=120, t_celsius=-3.15)
print(f'at 120 bara and -3.15 °C: z={z}, rho_m={rho_m}')

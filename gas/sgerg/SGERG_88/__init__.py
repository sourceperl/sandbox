"""
!!! WORK IN PROGRESS !!!


This code is based on the GERG-88 virial equation and requires coefficients
specific to the gas mixture being analyzed.

**Valid Input Ranges:**

- X3 (CO2 mole fraction): 0.0 to 0.3
- HS (calorific value in MJ/m^3 *): 20.0 to 48.0
- RM (relative density *): 0.55 to 0.9
- X5 (H2 mole fraction): 0.0 to 0.1
- P (pressure in bar): 0.0 to 120.0
- TC (temperature in degrees Celsius): -23.0 to 65.0

* metering at T = 0 °C and P = 1 ATM = 1.01325 bar, combustion at T = 25 °C

**Returned Values:**

- X2 (N2 mole fraction): Calculated value
- Z (compression factor)
- D (molar density in mol/m^3)
"""

from typing import Tuple

# some const
B11H0 = [-0.425468, 0.286500e-2, -0.462073e-5]
B11H1 = [0.877118e-3, -0.556281e-5, 0.881510e-8]
B11H2 = [-0.824747e-6, 0.431436e-8, -0.608319e-11]
B14 = [-5.21280e-2, 2.71570e-4, -2.5e-7]
B15 = [-0.521280e-1, 0.271570e-3, -0.25e-6]
B22 = [-0.144600, 0.740910e-3, -0.911950e-6]
B23 = [-0.339693, 0.161176e-2, -0.204429e-5]
B24 = [1.2e-2, 0.0, 0.0]
B33 = [-0.868340, 0.403760e-2, -0.516570e-5]
B44 = [-1.10596e-3, 8.13305e-5, -9.8722e-8]
B55 = [-0.110596e-2, 0.813385e-4, -0.987220e-7]

CR111H0 = [-0.302488, 0.195861e-2, -0.316302e-5]
CR111H1 = [0.646422e-3, -0.422876e-5, 0.688157e-8]
CR111H2 = [-0.332805e-6, 0.223160e-8, -0.367713e-11]
CR222 = [0.784980e-2, -0.398950e-4, 0.611870e-7]
CR223 = [0.552066e-2, -0.168609e-4, 0.157169e-7]
CR233 = [0.358783e-2, 0.806674e-5, -0.325798e-7]
CR333 = [0.205130e-2, 0.348880e-4, -0.837030e-7]
CR555 = [0.104711e-2, -0.364887e-5, 0.467095e-8]
CR117 = [0.736748e-2, -0.276578e-4, 0.343051e-7]

Z12 = 0.72
Z13 = -0.865
Y12 = 0.92
Y13 = 0.92
Y123 = 1.10
Y115 = 1.2

GM1R0 = -2.709328
GM1R1 = 0.021062199
# Molar Mass of N2 (kg/kmol)
MM_N2 = 28.0135
# Molar Mass of CO2 (kg/kmol)
MM_CO2 = 44.010
# Molar Mass of H2 (kg/kmol)
MM_H2 = 2.0159
# Molar Mass of CO (kg/kmol)
MM_CO = 28.010
# Molar volume (m3/kmol) of an ideal gas at standard temperature and pressure (also call STP for 0 °C and 1 ATM)
VM_STP = 22.414_097

FB = 22.710_811
# density in kg/m3 of dry air (at 0 °C and 1 ATM)
RHO_N_AIR = 1.292923
# 0°C in Kelvin
T_0C_K = 273.15
# Higher Heating Value (HHV) of H2 (MJ/kmol)
HHV_H2 = 285.83
# Higher Heating Value (HHV) of CO (MJ/kmol)
HHV_CO = 282.98


class SGERG:
    def __init__(self, hs: float, d: float = 0.610, x_co2: float = 0.0069, x_h2: float = 0.0):
        """
        SGERG class

        Args:
            hs (float): Calorific value in MJ/m^3 (20.0 to 48.0)
            d (float): Relative density (0.55 to 0.9)
            x_co2 (float): Mole fraction of CO2 (0.0 to 0.3)
            x_h2 (float): Mole fraction of H2 (0.0 to 0.1)
        """
        # public args
        self.hs = hs
        self.d = d
        self.x_co2 = x_co2
        self.x_h2 = x_h2

    @property
    def rho_n(self) -> float:
        """Gas density (kg/m³) at 0 °C and 1 ATM (also call Specific Mass)."""
        return self.d * RHO_N_AIR

    def _consistency_check(self):
        if not self.d > 0.55 + 0.97 * self.x_co2 - 0.45 * self.x_h2:
            raise ValueError('conflicting input')

    def run(self, p_bar: float, t_c: float):
        """
        Calculates the compression factor (Z) and molar density (D) of a natural gas
        using a simplified gas analysis and the GERG-88 virial equation.

        Args:
            p_bar (float): Pressure in bar (0.0 to 120.0).
            t_c (float): Temperature in degrees Celsius (-23.0 to 65.0).

        Return:
            z (float): Output compression factor (returned).
            d (float): Output molar density in mol/m^3 (returned).

        Raises:
            ValueError: If pressure (p) or temperature (tc) is outside the valid range.
        """
        # check args
        if not 0.0 < p_bar < 120.0:
            raise ValueError('pressure (p_bar) is out of range (0.0 to 120.0).')
        if not -23.0 < t_c < 65.0:
            raise ValueError('temperature (tc) is out of range (-23.0 to 65.0).')

        # check data consistency
        self._consistency_check()

        # 1. calculation of intermediate data
        x_ch, x_n2, x_co, h_ch = self._step1_calc_intermed_data()
        return x_ch, x_n2, x_co, h_ch

    def _step1_calc_intermed_data(self) -> Tuple[float, float, float, float]:
        """ step1 : compute x_ch, x_n2, x_co, h_ch """

        # internal function for iteration
        def _iter_calc(h_ch: float, x_co: float, md_stp: float) -> Tuple[float, float, float]:
            # molar mass of the equivalent hydrocarbon (kg/kmol)
            mm_ch = GM1R0 + GM1R1 * h_ch
            # molar fraction of the equivalent hydrocarbon
            x_ch = (self.hs - (self.x_h2 * HHV_H2 + x_co * HHV_CO) * md_stp) / h_ch / md_stp
            # molar fraction of nitrogen
            x_n2 = 1.0 - x_ch - self.x_co2 - self.x_h2 - x_co
            # gas density (kg/m3)
            rho_n = x_ch * mm_ch + x_n2 * MM_N2 + self.x_co2 * MM_CO2 + self.x_h2 * MM_H2 + x_co * MM_CO
            rho_n *= md_stp
            return rho_n, x_ch, x_n2

        # CO molar fraction from H2 molar fraction
        x_co = self.x_h2 * 0.0964

        # start points
        h_ch = 1000.0
        b_coef = -0.065
        # molar density (kmol/m3) under normal conditions for current B coef value
        md_stp = (VM_STP + b_coef)**-1

        # iteration 1
        for _ in range(20):
            rho_n_u, x_ch, x_n2 = _iter_calc(h_ch=h_ch, x_co=x_co, md_stp=md_stp)
            # convergence condition: diff between declared density and computed density is lower than 1e-6
            if not abs(self.rho_n - rho_n_u) > 1e-6:
                break
            rho_d, x_ch, x_n2 = _iter_calc(h_ch=h_ch + 1.0, x_co=x_co, md_stp=md_stp)
            dh_ch = (self.rho_n - rho_n_u)/(rho_d - rho_n_u)
            h_ch = h_ch + dh_ch
        else:
            ValueError('no convergency (step 1)')

        #
        b_coef = self._b(t=T_0C_K, b11=self._b11(t=T_0C_K, h=h_ch), x_ch=x_ch, x_n2=x_n2, x_co=x_co)

        # update molar density (kmol/m3)
        md_stp = (VM_STP + b_coef)**-1

        return x_ch, x_n2, x_co, h_ch

    def _b11(self, t: float, h: float) -> float:
        b11 = B11H0[0] + B11H0[1] * t + B11H0[2] * t**2
        b11 += (B11H1[0] + B11H1[1] * t + B11H1[2] * t**2) * h
        b11 += (B11H2[0] + B11H2[1] * t + B11H2[2] * t**2) * h**2
        return b11

    def _b(self, t: float, b11: float, x_ch: float, x_n2: float, x_co: float) -> float:
        """ Compute second virial coef Bn(v) """
        # mole fraction as x coefficients
        x1 = x_ch
        x2 = x_n2
        x3 = self.x_co2
        x4 = self.x_h2
        x5 = x_co
        # calculates second virial coefficients
        b14 = B14[0] + B14[1]*t + B14[2]*t**2
        b15 = B15[0] + B15[1]*t + B15[2]*t**2
        b22 = B22[0] + B22[1]*t + B22[2]*t**2
        b23 = B23[0] + B23[1]*t + B23[2]*t**2
        b24 = B24[0] + B24[1]*t + B24[2]*t**2
        b33 = B33[0] + B33[1]*t + B33[2]*t**2
        b44 = B44[0] + B44[1]*t + B44[2]*t**2
        b55 = B55[0] + B55[1]*t + B55[2]*t**2
        # specific case of b12 and b13
        b12 = (0.72 + 1.875e-5 * (320.0-t)**2) * (b11 + b22) / 2.0
        if b11 * b33 < 0.0:
            raise ValueError('no solution')
        b13 = -0.865 * (b11 * b33)**.5
        # compute B coefficient
        b = b11 * x1**2
        b += b12 * 2.0 * x1 * x2
        b += b13 * 2.0 * x1 * x3
        b += b14 * 2.0 * x1 * x4
        b += b15 * 2.0 * x1 * x5
        b += b22 * x2**2
        b += b23 * 2.0 * x2 * x3
        b += b24 * 2.0 * x2 * x4
        b += b33 * x3**2
        b += b44 * x4**2
        b += b55 * x5**2
        return b

    def cber(self, t, h, ceff):
        pass

    def iter(self, p, t, b, c, v, z):
        pass

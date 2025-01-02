"""
Calculates the compression factor (z) and molar density (d) of a natural gas
using a simplified gas analysis and the GERG-88 virial equation.

Usage:
    from SGERG_88 import SGERG

    sgerg = SGERG(hs=40.66, d=0.581, x_co2=0.006, x_h2=0.0)
    z, rho_m = sgerg.run(p_bar=60, t_celsius=-3.15)


Input Ranges:
- x_co2: CO2 mole fraction: 0.0 to 0.3
- hs: calorific value in MJ/m3 *): 20.0 to 48.0
- d: relative density *): 0.55 to 0.9
- x_h2: H2 mole fraction: 0.0 to 0.1
- p_bar: pressure in absolut bar: 0.0 to 120.0
- t_celsius: temperature in degrees Celsius: -23.0 to 65.0

* metering at t = 0 °C and p = 1 ATM = 1.01325 bar, combustion at t = 25 °C

Returned Value:
- z: compression factor
- rho_m: molar density (kmol/m3)
"""

from typing import Tuple

# some const
# thermal expansion coefficients Bxx (in m3/kmol if t in kelvin) of second virial coef B
BC11H0 = [-4.254_68e-1, 2.865_00e-3, -4.620_73e-6]
BC11H1 = [8.771_18e-4, -5.562_81e-6, 8.815_10e-9]
BC11H2 = [-8.247_47e-7, 4.314_36e-9, -6.083_19e-12]
BC14 = [-5.212_80e-2, 2.715_70e-4, -2.500_00e-7]
BC15 = [-6.872_90e-2, -2.393_81e-6, 5.181_95e-7]
BC22 = [-1.446_00e-1, 7.409_10e-4, -9.119_50e-7]
BC23 = [-3.396_93e-1, 1.611_76e-3, -2.044_29e-6]
BC24 = [1.200_00e-2, 0.000_00, 0.000_00]
BC33 = [-8.683_40e-1, 4.037_60e-3, -5.165_70e-6]
BC44 = [-1.105_96e-3, 8.133_85e-5, -9.872_20e-8]
BC55 = [-1.308_20e-1, 6.025_40e-4, -6.443_00e-7]

# thermal expansion coefficients Cxx (in m6/kmol2 if t in kelvin) of third virial coefficient C
CC111H0 = [-3.024_88e-1, 1.958_61e-3, -3.163_02e-6]
CC111H1 = [6.464_22e-4, -4.228_76e-6, 6.881_57e-9]
CC111H2 = [-3.328_05e-7, 2.231_60e-9, -3.677_13e-12]
CC222 = [7.849_80e-3, -3.989_50e-5, 6.118_70e-8]
CC333 = [2.051_30e-3, 3.488_80e-5, -8.370_30e-8]
CC115 = [7.36748e-3, -0.276578e-4, 0.343051e-7]
CC444 = [1.047_11e-3, -3.648_87e-6, 4.670_95e-9]
CC223 = [5.520_66e-3, -1.686_09e-5, 1.571_69e-8]
CC233 = [3.587_83e-3, 8.066_74e-6, -3.257_98e-8]

# ideal gas constant (MJ/kmol)
R_IDEAL_GAS = 0.0831451
# Molar Mass of N2 (kg/kmol)
MM_N2 = 28.0135
# Molar Mass of CO2 (kg/kmol)
MM_CO2 = 44.010
# Molar Mass of H2 (kg/kmol)
MM_H2 = 2.0159
# Molar Mass of CO (kg/kmol)
MM_CO = 28.010
# Molar volume (m3/kmol) of an ideal gas at standard temperature and pressure (0 °C and 1 ATM)
VM_N = 22.414_097

# density in kg/m3 of dry air (at 0 °C and 1 ATM)
RHO_N_AIR = 1.292_923
# 0°C in Kelvin
T_0C_K = 273.15
# Higher Heating Value of H2 (MJ/kmol)
H_H2 = 285.83
# Higher Heating Value of CO (MJ/kmol)
H_CO = 282.98


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

    def run(self, p_bar: float, t_celsius: float):
        """
        Calculates the compression factor (z) and molar density (d) of a natural gas
        using a simplified gas analysis and the GERG-88 virial equation.

        Args:
            p_bar (float): pressure in absolute bar (0.0 to 120.0)
            t_celsius (float): temperature in degrees Celsius (-23.0 to 65.0)

        Return:
            z (float): output compression factor
            rho_m (float): output molar density in mol/m3

        Raises:
            ValueError: If pressure (p_bar) or temperature (t_celsius) is outside the valid range.
        """
        # check args
        if not 0.0 <= p_bar <= 120.0:
            raise ValueError('pressure (p_bar) is out of range (0.0 to 120.0).')
        if not -23.0 <= t_celsius <= 65.0:
            raise ValueError('temperature (tc) is out of range (-23.0 to 65.0).')

        # input data must satisfy the following condition
        if not self.d > 0.55 + 0.97*self.x_co2 - 0.45*self.x_h2:
            raise ValueError('conflicting input')

        # 1. calculation of intermediate data
        x_ch, x_n2, x_co, h_ch = self._step1_calc_intermed_data()

        # intermediate calculated value for the N2 mole fraction satisfy the following conditions
        if not -0.01 <= x_n2 <= 0.5:
            raise ValueError('calculated value for the N2 mole fraction is out of range')
        if not x_n2 + self.x_co2 <= 0.5:
            raise ValueError('calculated value for the N2 + CO2 mole fraction is out of range')
        if not self.d > 0.55 + .4*x_n2 + 0.97*self.x_co2 - 0.45*self.x_h2:
            raise ValueError('internal inconsistency of input data')

        # 1. calculation of intermediate data
        x_ch, x_n2, x_co, h_ch = self._step1_calc_intermed_data()

        # 2. calculation of virial coefficients
        # find factors B and C of the virial equation z = 1 + B * rho_m + C * rho_m**2
        b_coef, c_coef = self._step2_calc_virial_coefs(t_celsius=t_celsius, h_ch=h_ch, x_ch=x_ch, x_n2=x_n2, x_co=x_co)

        # 3. calculation of compression factor and molar density
        z, rho_m = self._step3_calc_z_and_molar_density(p_bar=p_bar, t_celsius=t_celsius, b_coef=b_coef, c_coef=c_coef)

        return z, rho_m

    def _step1_calc_intermed_data(self) -> Tuple[float, float, float, float]:
        """ step1 : compute x_ch, x_n2, x_co, h_ch """

        # internal function for iteration
        def _iter_calc(h_ch: float, x_co: float, rho_m_n: float) -> Tuple[float, float, float]:
            # molar mass of the equivalent hydrocarbon (kg/kmol)
            mm_ch = -2.709_328 + 0.021_062_199 * h_ch
            # molar fraction of the equivalent hydrocarbon
            x_ch = (self.hs - (self.x_h2 * H_H2 + x_co * H_CO) * rho_m_n) / h_ch / rho_m_n
            # molar fraction of nitrogen
            x_n2 = 1.0 - x_ch - self.x_co2 - self.x_h2 - x_co
            # rho_n density (kg/m3): total molar mass (kg/kmol) * molar density (kmol/m3)
            mm_total = x_ch * mm_ch + x_n2 * MM_N2 + self.x_co2 * MM_CO2 + self.x_h2 * MM_H2 + x_co * MM_CO
            rho_n = mm_total * rho_m_n
            return rho_n, x_ch, x_n2

        # CO molar fraction from H2 molar fraction
        x_co = self.x_h2 * 0.0964

        # start points
        h_ch = 1000.0
        b_coef = -0.065
        # molar density (kmol/m3) under normal conditions for current B coef value
        rho_m_n = (VM_N + b_coef)**-1

        # iterations u and v
        u, v = 0, 0
        while True:
            while True:
                # iteration u
                u += 1
                if u > 20:
                    raise ValueError('no convergency (iteration u)')
                rho_n_u, x_ch, x_n2 = _iter_calc(h_ch=h_ch, x_co=x_co, rho_m_n=rho_m_n)
                # convergence condition: diff between declared density and computed density is lower than 1e-6
                if not abs(self.rho_n - rho_n_u) > 1e-6:
                    break
                rho_d, x_ch, x_n2 = _iter_calc(h_ch=h_ch + 1.0, x_co=x_co, rho_m_n=rho_m_n)
                dh_ch = (self.rho_n - rho_n_u)/(rho_d - rho_n_u)
                h_ch = h_ch + dh_ch
            # iteration v
            v += 1
            if v > 20:
                raise ValueError('no convergency (iteration v)')
            b_coef = self._b_coef(t_kelvin=T_0C_K, h_ch=h_ch, x_ch=x_ch, x_n2=x_n2, x_co=x_co)
            # update molar density (kmol/m3)
            rho_m_n = (VM_N + b_coef)**-1
            # calculation of the higher calorific value of the gas (MJ/m3)
            hs_v = (x_ch*h_ch + x_co*H_CO + self.x_h2*H_H2) * rho_m_n
            # convergence condition: measured higher calorific value Hs vs calculated calorific value Hs(v)
            if abs(self.hs - hs_v) < 1e-4:
                break

        # return molar fract: equivalent hydrocarbon (x_ch), nitrogen (x_n2), carbon monoxide (x_co) and
        # molar calorific value (MJ/kmol) of the equivalent hydrocarbon (h_ch)
        return x_ch, x_n2, x_co, h_ch

    def _step2_calc_virial_coefs(self, t_celsius: float, h_ch: float,
                                 x_ch: float, x_n2: float, x_co: float) -> Tuple[float, float]:
        """ step2 : compute virial coefficients B and C """

        # t celsius to kelvin
        t_kelvin = t_celsius + T_0C_K

        # b and c coef for current temperature
        b_coef = self._b_coef(t_kelvin=t_kelvin, h_ch=h_ch, x_ch=x_ch, x_n2=x_n2, x_co=x_co)
        c_coef = self._c_coef(t_kelvin=t_kelvin, h_ch=h_ch, x_ch=x_ch, x_n2=x_n2, x_co=x_co)

        return b_coef, c_coef

    def _step3_calc_z_and_molar_density(self, p_bar: float, t_celsius: float,
                                        b_coef: float, c_coef: float, ) -> Tuple[float, float]:
        """ step3 : compute z and molar density (kmol/m3) """

        # t celsius to kelvin
        t_kelvin = t_celsius + T_0C_K
        rt = R_IDEAL_GAS * t_kelvin
        # rho_m(w=0)
        rho_m = (rt / p_bar + b_coef)**-1
        # iteration w
        w = 0
        while True:
            # avoid infinite loop
            w += 1
            if w > 20:
                raise ValueError('no convergency (iteration w)')
            # rho_m(w)=(RT/p)(1 + B x rho_m(w-1) + C x rho_m(w-1)**2)
            rho_m = ((rt / p_bar) * (1 + b_coef * rho_m + c_coef * rho_m**2))**-1
            # z(w) = 1 + B.rho_m(w) + C.rho_m(w)**2
            z = 1 + b_coef * rho_m + c_coef * rho_m**2
            # calculated pressure = (n/V) x R x T x Z where (n/V) = rho_m (molar density)
            p_w = rho_m * rt * z
            # convergence condition: measured pressure vs calculated pressure lower than 10**-5
            if abs(p_bar - p_w) < 1e-5:
                break
        # apply the roundings
        z = round(z, 5)
        rho_m = round(rho_m, 3)
        return z, rho_m

    def _b_coef(self, t_kelvin: float, h_ch: float, x_ch: float, x_n2: float, x_co: float) -> float:
        """ Compute second virial coef B """
        # calculates second virial coefficients (with thermal expansion coefficients BCxx[x])
        b14 = BC14[0] + BC14[1]*t_kelvin + BC14[2]*t_kelvin**2
        b15 = BC15[0] + BC15[1]*t_kelvin + BC15[2]*t_kelvin**2
        b22 = BC22[0] + BC22[1]*t_kelvin + BC22[2]*t_kelvin**2
        b23 = BC23[0] + BC23[1]*t_kelvin + BC23[2]*t_kelvin**2
        b24 = BC24[0] + BC24[1]*t_kelvin + BC24[2]*t_kelvin**2
        b33 = BC33[0] + BC33[1]*t_kelvin + BC33[2]*t_kelvin**2
        b44 = BC44[0] + BC44[1]*t_kelvin + BC44[2]*t_kelvin**2
        b55 = BC55[0] + BC55[1]*t_kelvin + BC55[2]*t_kelvin**2
        # specific case of b11
        b11 = BC11H0[0] + BC11H0[1] * t_kelvin + BC11H0[2] * t_kelvin**2
        b11 += (BC11H1[0] + BC11H1[1] * t_kelvin + BC11H1[2] * t_kelvin**2) * h_ch
        b11 += (BC11H2[0] + BC11H2[1] * t_kelvin + BC11H2[2] * t_kelvin**2) * h_ch**2
        # specific case of b12
        b12 = (0.72 + 1.875e-5 * (320.0-t_kelvin)**2) * (b11 + b22) / 2.0
        if b11 * b33 < 0.0:
            raise ValueError('no solution')
        # specific case of b13
        b13 = -0.865 * (b11 * b33)**.5
        # compute B coefficient: apply thermal expansion coefficients
        b = b11 * x_ch**2
        b += b12 * 2.0 * x_ch * x_n2
        b += b13 * 2.0 * x_ch * self.x_co2
        b += b14 * 2.0 * x_ch * self.x_h2
        b += b15 * 2.0 * x_ch * x_co
        b += b22 * x_n2**2
        b += b23 * 2.0 * x_n2 * self.x_co2
        b += b24 * 2.0 * x_n2 * self.x_h2
        b += b33 * self.x_co2**2
        b += b44 * self.x_h2**2
        b += b55 * x_co**2
        return b

    def _c_coef(self, t_kelvin: float, h_ch: float, x_ch: float, x_n2: float, x_co: float):
        """ Compute the third virial coefficient C """
        # calculates third virial coefficients (with thermal expansion coefficients CCxx[x])
        c222 = CC222[0] + CC222[1]*t_kelvin + CC222[2]*t_kelvin**2
        c333 = CC333[0] + CC333[1]*t_kelvin + CC333[2]*t_kelvin**2
        c444 = CC444[0] + CC444[1]*t_kelvin + CC444[2]*t_kelvin**2
        c115 = CC115[0] + CC115[1]*t_kelvin + CC115[2]*t_kelvin**2
        c223 = CC223[0] + CC223[1]*t_kelvin + CC223[2]*t_kelvin**2
        c233 = CC233[0] + CC233[1]*t_kelvin + CC233[2]*t_kelvin**2
        # specific cases
        # c111
        c111 = CC111H0[0] + CC111H0[1]*t_kelvin + CC111H0[2]*t_kelvin**2
        c111 += (CC111H1[0] + CC111H1[1]*t_kelvin + CC111H1[2]*t_kelvin**2) * h_ch
        c111 += (CC111H2[0] + CC111H2[1]*t_kelvin + CC111H2[2]*t_kelvin**2) * h_ch**2
        # c112
        c112 = (0.92 + 0.0013 * (t_kelvin - 270.0)) * (c111 * c111 * c222)**(1/3)
        # c113
        c113 = 0.92 * (c111 * c111 * c333)**(1/3)
        # c114
        c114 = 1.20 * (c111 * c111 * c444)**(1/3)
        # c122
        c122 = (0.92 + 0.0013 * (t_kelvin - 270.0)) * (c111 * c222 * c222)**(1/3)
        # c123
        c123 = 1.10 * (c111 * c222 * c333)**(1/3)
        # c133
        c133 = 0.92 * (c111 * c333 * c333)**(1/3)
        # c coef
        c = x_ch**3 * c111
        c += 3.0 * x_ch**2 * x_n2 * c112
        c += 3.0 * x_ch**2 * self.x_co2 * c113
        c += 3.0 * x_ch**2 * self.x_h2 * c114
        c += 3.0 * x_ch**2 * x_co * c115
        c += 3.0 * x_ch * x_n2**2 * c122
        c += 6.0 * x_ch * x_n2 * self.x_co2 * c123
        c += 3.0 * x_ch * self.x_co2**2 * c133
        c += x_n2**3 * c122
        c += 3.0 * x_n2**2 * self.x_co2 * c223
        c += 3.0 * x_n2 * self.x_co2**2 * c233
        c += self.x_co2**3 * c333
        c += self.x_h2**3 * c444
        return c

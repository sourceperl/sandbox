from math import sqrt

# some const
PRES_REF_KPA = 101.325
TEMP_REF_K = 273.15
R = 8.314_51
M_AIR = 28.962_6


class ISO_6976:
    def __init__(self, x_as_ratio: bool = False, x_n2: float = 0.0, x_o2: float = 0.0, x_co2: float = 0.0,
                 x_h2: float = 0.0, x_ch4: float = 0.0, x_c2h6: float = 0.0, x_c3h8: float = 0.0,
                 x_iso_c4h10: float = 0.0, x_n_c4h10: float = 0.0, x_iso_c5h12: float = 0.0, x_n_c5h12: float = 0.0,
                 x_neo_c5h12: float = 0.0, x_n_c6h14: float = 0.0) -> None:
        """ 
        SGERG class

        Args:
            x_as_ratio (bool): X-components are expressed as ratios when x_as_ratio is True (default is percent)
            x_n2 (float): Mole fraction of Nitrogen
            x_o2 (float): Mole fraction of Oxygen
            x_co2 (float): Mole fraction of Carbon Dioxide
            x_h2 (float): Mole fraction of Hydrogen
            x_ch4 (float): Mole fraction of Methane
            x_c2h6 (float): Mole fraction of Ethane
            x_c3h8 (float): Mole fraction of Propane
            x_iso_c4h10 (float): Mole fraction of IsoButane (or 2-methylpropane)
            x_n_c4h10 (float): Mole fraction of n-Butane
            x_iso_c5h12 (float): Mole fraction of IsoPentane (or 2-methylbutane)
            x_n_c5h12 (float): Mole fraction of n-Pentane
            x_neo_c5h12 (float): Mole fraction of Neopentane (2,2-Dimethylpropane)
            x_n_c6h14 (float): Mole fraction of n-Hexane
        """
        self.x_as_ratio = x_as_ratio
        self.x_n2 = x_n2
        self.x_o2 = x_o2
        self.x_co2 = x_co2
        self.x_h2 = x_h2
        self.x_ch4 = x_ch4
        self.x_c2h6 = x_c2h6
        self.x_c3h8 = x_c3h8
        self.x_iso_c4h10 = x_iso_c4h10
        self.x_n_c4h10 = x_n_c4h10
        self.x_iso_c5h12 = x_iso_c5h12
        self.x_n_c5h12 = x_n_c5h12
        self.x_neo_c5h12 = x_neo_c5h12
        self.x_n_c6h14 = x_n_c6h14

    @property
    def x_sum(self) -> float:
        _sum = self.x_n2 + self.x_o2 + self.x_co2 + self.x_h2 + self.x_ch4 + self.x_c2h6 + self.x_c3h8
        _sum += self.x_iso_c4h10 + self.x_n_c4h10 + self.x_iso_c5h12 + self.x_n_c5h12
        _sum += self.x_neo_c5h12 + self.x_n_c6h14
        return _sum

    @property
    def z0(self) -> float:
        """Compression factor at standard condition (0°C and 1 ATM)."""
        z_sum = 0.022_4 * self.x_n2
        z_sum += 0.031_6 * self.x_o2
        z_sum += 0.081_9 * self.x_co2
        z_sum += -0.004_0 * self.x_h2
        z_sum += 0.049_0 * self.x_ch4
        z_sum += 0.100_0 * self.x_c2h6
        z_sum += 0.145_3 * self.x_c3h8
        z_sum += 0.206_9 * self.x_n_c4h10
        z_sum += 0.204_9 * self.x_iso_c4h10
        z_sum += 0.286_4 * self.x_n_c5h12
        z_sum += 0.251_0 * self.x_iso_c5h12
        z_sum += 0.238_7 * self.x_neo_c5h12
        z_sum += 0.328_6 * self.x_n_c6h14
        if not self.x_as_ratio:
            z_sum /= 100
        return 1 - z_sum**2

    @property
    def hhv_kj(self) -> float:
        """Higher heating value (in kj/nm3)."""
        hhv_kj_sum = 0 * self.x_n2
        hhv_kj_sum += 0 * self.x_o2
        hhv_kj_sum += 0 * self.x_co2
        hhv_kj_sum += 12_788 * self.x_h2
        hhv_kj_sum += 39_840 * self.x_ch4
        hhv_kj_sum += 69_790 * self.x_c2h6
        hhv_kj_sum += 99_220 * self.x_c3h8
        hhv_kj_sum += 128_660 * self.x_n_c4h10
        hhv_kj_sum += 128_230 * self.x_iso_c4h10
        hhv_kj_sum += 158_070 * self.x_n_c5h12
        hhv_kj_sum += 157_760 * self.x_iso_c5h12
        hhv_kj_sum += 157_120 * self.x_neo_c5h12
        hhv_kj_sum += 187_530 * self.x_n_c6h14
        if not self.x_as_ratio:
            hhv_kj_sum /= 100
        return hhv_kj_sum / self.z0

    @property
    def hhv_wh(self) -> float:
        """Higher heating value (in wh/nm3)."""
        return self.hhv_kj / 3.6

    @property
    def lhv_kj(self) -> float:
        """Lower heating value (in kj/nm3)."""
        lhv_kj_sum = 0 * self.x_n2
        lhv_kj_sum += 0 * self.x_o2
        lhv_kj_sum += 0 * self.x_co2
        lhv_kj_sum += 10_777 * self.x_h2
        lhv_kj_sum += 35_818 * self.x_ch4
        lhv_kj_sum += 63_760 * self.x_c2h6
        lhv_kj_sum += 91_180 * self.x_c3h8
        lhv_kj_sum += 118_610 * self.x_n_c4h10
        lhv_kj_sum += 118_180 * self.x_iso_c4h10
        lhv_kj_sum += 146_000 * self.x_n_c5h12
        lhv_kj_sum += 145_690 * self.x_iso_c5h12
        lhv_kj_sum += 145_060 * self.x_neo_c5h12
        lhv_kj_sum += 173_450 * self.x_n_c6h14
        if not self.x_as_ratio:
            lhv_kj_sum /= 100
        return lhv_kj_sum / self.z0

    @property
    def lhv_wh(self) -> float:
        """Lower heating value (in wh/nm3)."""
        return self.lhv_kj / 3.6

    @property
    def density(self) -> float:
        """Density (volumetric mass density or specific mass): mass per unit of volume (in kg/nm3)."""
        d_comp_coef = PRES_REF_KPA/(R*TEMP_REF_K)
        density_sum = 28.013_5 * d_comp_coef * self.x_n2
        density_sum += 31.998_8 * d_comp_coef * self.x_o2
        density_sum += 44.010 * d_comp_coef * self.x_co2
        density_sum += 2.015_9 * d_comp_coef * self.x_h2
        density_sum += 16.043 * d_comp_coef * self.x_ch4
        density_sum += 30.070 * d_comp_coef * self.x_c2h6
        density_sum += 44.097 * d_comp_coef * self.x_c3h8
        density_sum += 58.123 * d_comp_coef * self.x_n_c4h10
        density_sum += 58.123 * d_comp_coef * self.x_iso_c4h10
        density_sum += 72.150 * d_comp_coef * self.x_n_c5h12
        density_sum += 72.150 * d_comp_coef * self.x_iso_c5h12
        density_sum += 72.150 * d_comp_coef * self.x_neo_c5h12
        density_sum += 86.177 * d_comp_coef * self.x_n_c6h14
        if not self.x_as_ratio:
            density_sum /= 100
        return density_sum / self.z0

    @property
    def rel_density(self) -> float:
        """Relative density (or specific gravity): ratio of the density (mass of a unit volume) vs air."""
        rel_density_sum = (28.013_5 / M_AIR) * self.x_n2
        rel_density_sum += (31.998_8 / M_AIR) * self.x_o2
        rel_density_sum += (44.010 / M_AIR) * self.x_co2
        rel_density_sum += (2.015_9 / M_AIR) * self.x_h2
        rel_density_sum += (16.043 / M_AIR) * self.x_ch4
        rel_density_sum += (30.070 / M_AIR) * self.x_c2h6
        rel_density_sum += (44.097 / M_AIR) * self.x_c3h8
        rel_density_sum += (58.123 / M_AIR) * self.x_n_c4h10
        rel_density_sum += (58.123 / M_AIR) * self.x_iso_c4h10
        rel_density_sum += (72.150 / M_AIR) * self.x_n_c5h12
        rel_density_sum += (72.150 / M_AIR) * self.x_iso_c5h12
        rel_density_sum += (72.150 / M_AIR) * self.x_neo_c5h12
        rel_density_sum += (86.177 / M_AIR) * self.x_n_c6h14
        if not self.x_as_ratio:
            rel_density_sum /= 100
        return 0.999_41 * rel_density_sum / self.z0

    @property
    def wobbe(self) -> float:
        """Wobbe index (wh/nm3)."""
        return self.hhv_wh/sqrt(self.rel_density)

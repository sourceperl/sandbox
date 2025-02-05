import math


def get_vol_humidity(dew_point_c: float, p_bara: float) -> float:
    """ 
    Compute the volumetric humidity in mg/nm3.

    Args:
        dew_point_c (float): dew point in degrees Celsius
        p_bara (float): pressure in absolute bar
    """
    a = 4.8309e3 * math.exp(7.5515e-2 * dew_point_c - 4.0637e-4 * dew_point_c**2 + 1.8097e-6 * dew_point_c**3)
    b = 3.3716e1 * math.exp(9.7971e-2 * dew_point_c - 9.9324e-4 * dew_point_c**2 + 5.3630e-6 * dew_point_c**3)
    c = 8.5171e-2 + p_bara**1.0359 + 3.7130e-5 * p_bara**3.0963
    return (a/c) + b


def get_dew_point_c(vol_hum_mg: float, p_bara: float) -> float:
    """
    Compute the dew point in degrees Celsius.

    Args:
        vol_hum_mg (float): volumetric humidity in mg/nm3
        p_bara (float): pressure in absolute bar
    """
    a_poly = (1.023e1 + 1.811e-3 * vol_hum_mg - 9.711e-8 * vol_hum_mg**2 + 1.450e-12 * vol_hum_mg**3)
    a = a_poly * math.log(p_bara) + 1.049e1 * math.log(vol_hum_mg) - 8.990e1
    b = -8.325e-2 + 1.063 * a + 1.821e-3 * a**2 - 2.790e-5 * a**3
    return b

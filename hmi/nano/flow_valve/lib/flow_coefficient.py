#!/usr/bin/env python3

"""
Some function to deal with Cv flow coefficient of gas valve.

https://www.swagelok.com/downloads/webcatalogs/EN/MS-06-84.pdf
"""


import math


# some functions
def celsius_to_kelvin(deg_c: float) -> float:
    """Conversion from degree Celsius to Kelvin"""
    return deg_c + 273.15


def is_subsonic(p_up_bara: float, p_down_bara: float) -> bool:
    """Obtain subsonic state for current pressures"""
    return p_down_bara > p_up_bara / 2


def valve_flow(cv: float, p1_bara: float, p2_bara: float, t_deg_c: float = 6.0, sg: float = 0.554) -> float:
    """Compute flow rate (nm3/h) in a valve from it's Cv"""
    # check args value
    if p1_bara < 0.00:
        raise ValueError('arg p1_bara must be positive')
    if p2_bara < 0.00:
        raise ValueError('arg p2_bara must be positive')
    # formats args for calculation
    t_k = celsius_to_kelvin(t_deg_c)
    sign = 1 if p1_bara - p2_bara >= 0 else -1
    p_up = max(p1_bara, p2_bara)
    p_down = min(p1_bara, p2_bara)
    dp = p_up - p_down
    # circulation below or over critical point
    if is_subsonic(p_up, p_down):
        return sign * 417 * cv * p_up * (1 - ((2 * dp) / (3 * p_up))) * math.sqrt(dp / (p_up * sg * t_k))
    else:
        return sign * 0.471 * 417 * cv * p_up * math.sqrt(1 / (sg * t_k))


def valve_cv(q_nm3_h: float, p_up_bara: float, p_down_bara: float, t_deg_c: float = 6.0, sg: float = 0.554) -> float:
    """Compute Cv of a valve from its flow rate (nm3/h)"""
    # formats args for calculation
    t_k = celsius_to_kelvin(t_deg_c)
    dp = p_up_bara - p_down_bara
    # circulation below or over critical point
    if is_subsonic(p_up_bara, p_down_bara):
        denom = 417 * p_up_bara * (1 - ((2 * dp) / (3 * p_up_bara))) * math.sqrt(dp / (p_up_bara * sg * t_k))
        return q_nm3_h / denom
    else:
        return q_nm3_h / (0.471 * 417 * p_up_bara * math.sqrt(1 / (sg * t_k)))

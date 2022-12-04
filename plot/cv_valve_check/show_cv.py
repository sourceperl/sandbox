#!/usr/bin/env python3

"""
Some function to deal with Cv flow coefficient of gas valve.

https://www.swagelok.com/downloads/webcatalogs/EN/MS-06-84.pdf
"""

import csv
import math
import matplotlib.pyplot as plt


# some functions
def celsius_to_kelvin(deg_c: float) -> float:
    """Conversion from degree Celsius to Kelvin"""
    return deg_c + 273.15


def is_subsonic(p_up_bara: float, p_down_bara: float) -> bool:
    """Obtain subsonic state for current pressures"""
    return p_down_bara > p_up_bara / 2


def valve_flow(cv: float, p_up_bara: float, p_down_bara: float, t_deg_c: float = 6.0, sg: float = 0.554) -> float:
    """Compute flow rate (nm3/h) in a valve from it's Cv"""
    t_k = celsius_to_kelvin(t_deg_c)
    dp_bar = p_up_bara - p_down_bara
    # circulation below or over critical point
    if is_subsonic(p_up_bara, p_down_bara):
        return 417 * cv * p_up_bara * (1 - ((2 * dp_bar) / (3 * p_up_bara))) * \
               math.sqrt(dp_bar / (p_up_bara * sg * t_k))
    else:
        return 0.471 * 417 * cv * p_up_bara * math.sqrt(1 / (sg * t_k))


def valve_cv(q_nm3_h: float, p_up_bara: float, p_down_bara: float, t_deg_c: float = 6.0, sg: float = 0.554) -> float:
    """Compute Cv of a valve from its flow rate (nm3/h)"""
    t_k = celsius_to_kelvin(t_deg_c)
    dp_bar = p_up_bara - p_down_bara
    # circulation below or over critical point
    if is_subsonic(p_up_bara, p_down_bara):
        return q_nm3_h / (417 * p_up_bara * (1 - ((2 * dp_bar) / (3 * p_up_bara))) *
                          math.sqrt(dp_bar / (p_up_bara * sg * t_k)))
    else:
        return q_nm3_h / (0.471 * 417 * p_up_bara * math.sqrt(1 / (sg * t_k)))


if __name__ == '__main__':
    # load csv data
    pos_l, qi_l, qt_l = [], [], []
    with open('valve_data.csv', 'r') as f:
        for row in csv.DictReader(f, delimiter=';'):
            pos = float(row['Position VL']) / 10
            pos_l.append(pos)
            qi = float(row['Qi'])
            qi_l.append(qi)
            dp = (float(row['P amont']) / 10) - (float(row['P aval']) / 10)
            p_amt = float(row['P amont']) / 10
            p_avl = float(row['P aval']) / 10
            qt = valve_flow(cv=48 * pos / 100, p_up_bara=p_amt, p_down_bara=p_avl)
            qt_l.append(qt)

    # plot it
    plt.scatter(pos_l, qi_l, marker='o', label='Meter flow')
    plt.scatter(pos_l, qt_l, marker='^', label='Calculated flow')
    plt.xlabel('Position (%)')
    plt.ylabel('Q (nm3/h)')
    plt.legend()
    plt.grid()
    plt.show()

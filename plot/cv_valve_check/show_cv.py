import csv
import matplotlib.pyplot as plt
import math


# some functions
def celsius_to_kelvin(deg_c):
    return deg_c + 273.15


def is_subsonic(p_up_bara, p_down_bara):
    return p_down_bara > p_up_bara / 2


def valve_flow(cv, p_up_bara, p_down_bara, position=100.0, t_deg_c=8.0, sg=0.64):
    # compute flow in linear process valve
    t_deg_k = celsius_to_kelvin(t_deg_c)
    kv = 0.857 * cv
    # circulation below or over critical point
    if is_subsonic(p_up_bara, p_down_bara):
        delta_p_bar = p_up_bara - p_down_bara
        q_nm3_h = 514 * kv * (position / 100.0) * math.sqrt((delta_p_bar * p_down_bara) / (sg * t_deg_k))
    else:
        q_nm3_h = 257 * kv * (position / 100.0) * p_up_bara * 1 / math.sqrt(sg * t_deg_k)
    return q_nm3_h


def valve_cv(q_nm3_h, p_up_bara, p_down_bara, position=100.0, t_deg_c=8.0, sg=0.64):
    # compute cv for a linear process valve
    t_deg_k = celsius_to_kelvin(t_deg_c)
    delta_p_bar = p_up_bara - p_down_bara
    # circulation below or over critical point
    if is_subsonic(p_up_bara, p_down_bara):
        kv = q_nm3_h * (100.0 / (514 * position)) * math.sqrt((sg * t_deg_k) / (delta_p_bar * p_down_bara))
    else:
        kv = q_nm3_h * (100.0 / (257 * p_up_bara * position)) * math.sqrt(sg * t_deg_k)
    cv = kv / 0.857
    return cv


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
            qt = valve_flow(cv=48, p_up_bara=p_amt, p_down_bara=p_avl, position=pos)
            qt_l.append(qt)

    # plot it
    plt.scatter(pos_l, qi_l, marker='o', label='Qi')
    plt.scatter(pos_l, qt_l, marker='^', label='Qt')
    plt.xlabel('Position (%)')
    plt.ylabel('Q (nm3/h)')
    plt.legend()
    plt.grid()
    plt.show()

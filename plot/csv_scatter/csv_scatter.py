#!/usr/bin/env python3

"""
Draw a Scatter with 2 list of data (in CSV files). 
"""


from pprint import pprint
from collections import defaultdict
# apt install python3-dateutil
from dateutil import parser
from os.path import abspath, dirname, join
# apt install python3-matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm


# params
class CSV_FILES:
    x_file: str = 'data/l2.csv'
    x_id: str = 'L2'
    y_file: str = 'data/l1.csv'
    y_id: str = 'L1'


# some functions
def linspace(a, b, n=100):
    if n < 2:
        return b
    diff = (float(b) - a)/(n - 1)
    return [diff * i + a  for i in range(n)]


# load data from csv files to dict
my_data_d = defaultdict(dict)
for csv_file, data_id in ((CSV_FILES.x_file, CSV_FILES.x_id), (CSV_FILES.y_file, CSV_FILES.y_id)):
    csv_file_abs_path = join(dirname(abspath(__file__)), csv_file)
    with open(csv_file_abs_path, 'r') as file:
        for line_idx, line in enumerate(file, start=1):
            if line_idx > 10_000:
                break
            line = line.strip()
            if line:
                try:
                    # decode data format like "2024-01-01 12:10:00,12.783 K"
                    raw_date, value = (line.strip().split(','))
                    measure_dt = parser.parse(raw_date, fuzzy=True)
                    measure_value, suffix = value.split(' ')
                    measure_value = float(measure_value)
                    #if suffix.upper() == 'K':
                    #    measure_value *= 1_000
                    my_data_d[measure_dt][data_id] = measure_value
                except ValueError:
                    pass
                    #print(f'unable to parse line "{line}"')

# debug
#pprint(my_data_d)

# show result
hour2color_l = cm.rainbow(linspace(0, 1, n=24))
for data_dt, values_d in my_data_d.items():
    plt.scatter(values_d[CSV_FILES.x_id], values_d[CSV_FILES.y_id], color=hour2color_l[data_dt.hour])

# draw lines
plt.plot([12.00, 13.00], [12.00, 13.00], 'g--')
plt.fill_between([12.00, 13.00], [12.00, 13.00], [12.10, 13.10], alpha=0.1, color='r')
plt.fill_between([12.00, 13.00], [12.00, 13.00], [11.90, 12.90], alpha=0.1, color='b')

# add some labels
plt.grid(visible=True)
plt.title('Gas analyzer comparison')
plt.xlabel(CSV_FILES.x_id)
plt.ylabel(CSV_FILES.y_id)

# show result
plt.show()

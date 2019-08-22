#!/usr/bin/env python3

# Create simplified version of "Gantt chart" from well named vars "prj_name" and "tasks_cnf"

from collections import OrderedDict
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DAILY, DateFormatter, rrulewrapper, RRuleLocator, date2num
import numpy as np

# project name
prj_name = 'My wonderful project'

# tasks config: task name, start date, end date, task color (optional)
tasks_cnf = """
Task 1, 07-10-2019, 11-10-2019
Task 2, 14-10-2019, 18-10-2019, orange
Task 3, 21-10-2019, 25-10-2019, red
Task 4, 09-10-2019, 15-10-2019, turquoise
"""

# parse tasks string
tasks_d = OrderedDict()

for task_line in map(str.strip, tasks_cnf.split('\n')):
    # skip comment or blank line
    if not task_line.startswith('#') and task_line.split():
        str_tokens = list(map(str.strip, task_line.split(',')))
        task_lbl, start_date, end_date = str_tokens[:3]
        try:
            task_color = str_tokens[3]
        except IndexError:
            task_color = 'olive'
        tasks_d[task_lbl] = [datetime.strptime(start_date, '%d-%m-%Y'),
                             datetime.strptime(end_date, '%d-%m-%Y'),
                             task_color]

# create subplot
fig = plt.figure(figsize=(20, 8))
ax = fig.add_subplot(111)

# add barh to current subplot ax
barh_i = 0
for task_name, (start_date, end_date, color) in tasks_d.items():
    start_num, end_num = map(date2num, (start_date, end_date))
    ax.barh((barh_i * 0.5) + 0.5, end_num - start_num + 1, left=start_num, height=0.3, align='center',
            color=color, alpha=0.8)
    barh_i += 1

# create y ticks with tasks labels
pos = np.arange(0.5, len(tasks_d) * 0.5 + 0.5, 0.5)
plt.yticks(pos, tasks_d.keys())

# x axis job
ax.xaxis.set_major_locator(RRuleLocator(rrulewrapper(DAILY, interval=1)))
ax.xaxis.set_major_formatter(DateFormatter('%d-%b-%y'))
fig.autofmt_xdate()

# y axis job
ax.set_ylim(ymin=-0.1, ymax=len(tasks_d) * 0.5 + 0.5)
ax.invert_yaxis()

# add grid
ax.grid(linestyle=':')

# add title
plt.title(prj_name)

# output
# plt.savefig('out.svg')
plt.show()

#!/usr/bin/env python3

import time
from random import random
from pyPromLib.endpoints import MetricsHttpSrv
from pyPromLib.metrics import Metric, MetricType


# start HTTP server
metrics_srv = MetricsHttpSrv(bind='127.0.0.1', port=8080)
metrics_srv.start()

# add metrics
my_metric_ratio = Metric('my_metric_ratio', MetricType.GAUGE, comment='a gauge metric')
my_metric_total = Metric('my_metric_total', MetricType.COUNTER, comment='a counter metric')
my_metric_histo = Metric('my_metric_histo', MetricType.HISTOGRAM, comment='an histo metric')
my_metric_sumy = Metric('my_metric_sumy', MetricType.SUMMARY, comment='a summary metric')

# share this metrics with http server
metrics_srv.add(my_metric_ratio)
metrics_srv.add(my_metric_total)
metrics_srv.add(my_metric_histo)
metrics_srv.add(my_metric_sumy)

# main loop
loop_count = 0
while True:
    loop_count += 1
    my_metric_ratio.set(0.42, labels_d={'foo': 'const'})
    my_metric_ratio.set(round(random(), 4), labels_d={'foo': 'rand'})
    my_metric_total.set(loop_count, labels_d={'foo': 'loop'})
    my_metric_histo.set({'0.05': 24054, '0.1': 33444, '0.2': 100392, '0.5': 129389, '1': 133988,
                         'sum': 53423, 'count': 144320})
    my_metric_sumy.set({'0.01': 3102, '0.05': 3272, '0.5': 4773, '0.9': 9001, '0.99': 76656,
                        'sum': 1.7560473e+07, 'count': 2693})
    time.sleep(1.0)
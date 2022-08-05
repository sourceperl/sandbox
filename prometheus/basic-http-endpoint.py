#!/usr/bin/env python3

import time
from random import random
from pyPromLib.endpoints import MetricsHttpSrv
from pyPromLib.metrics import Metric, MetricType


# start HTTP server
metrics_srv = MetricsHttpSrv(bind='127.0.0.1', port=8080)
metrics_srv.start()

# add metrics
my_random_metric = Metric('my_random_metric', MetricType.GAUGE, comment='a random gauge metric for testing purposes')

# share this metrics with http server
metrics_srv.add(my_random_metric)

# main loop
while True:
    my_random_metric.set(round(100 * random(), 2))
    time.sleep(1.0)
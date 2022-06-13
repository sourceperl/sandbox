#!/usr/bin/env python3

"""Prometheus HTTP endpoint template."""

from enum import Enum
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread, Lock
from typing import Any
import time


class MetricType(Enum):
    """Definition of metric types."""
    counter = 'counter'
    gauge = 'gauge'
    histogram = 'histogram'
    summary = 'summary'
    untyped = 'untyped'


@dataclass
class Metric:
    """A Prometheus Metric."""
    name: str
    value: Any = None
    type: MetricType = MetricType.untyped
    comment: str = ''


class MetSrvShare:
    """Threads share area."""
    # public
    srv_lock = Lock()
    # private
    _metrics_l = list()

    @classmethod
    def add(cls, metric: Metric):
        """Add metric to server share list."""
        with cls.srv_lock:
            cls._metrics_l.append(metric)

    @classmethod
    def remove(cls, metric: Metric):
        """Remove metric from server share list."""
        with cls.srv_lock:
            cls._metrics_l.remove(metric)

    @classmethod
    def as_list(cls) -> list:
        """Metrics in a thread safe list."""
        with cls.srv_lock:
            return cls._metrics_l.copy()


class HandleRequests(BaseHTTPRequestHandler):
    """Custom HTTP handler"""

    def version_string(self):
        """Replace default server banner."""
        return 'self-service here ;-)'

    def log_message(self, format: str, *args: Any) -> None:
        """Replace log_message to turn off log msg."""
        return None

    def do_GET(self):
        """Process HTTP GET request."""
        if self.path == '/metrics':
            # prometheus scrap endpoint
            # headers
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            # body
            msg = ''
            for metric in MetSrvShare.as_list():
                if metric.value is not None:
                    if metric.comment:
                        msg += f'# HELP {metric.name} Comment line for {metric.comment}\n'
                    if metric.type is not MetricType.untyped:
                        msg += f'# TYPE {metric.name} {metric.type.value}\n'
                    msg += f'{metric.name} {metric.value}\n'
            self.wfile.write(msg.encode('utf-8'))
        else:
            # nothing for you here
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    # start HTTP server as a thread
    http_srv = ThreadingHTTPServer(('0.0.0.0', 8080), HandleRequests)
    http_srv_th = Thread(target=http_srv.serve_forever, daemon=True)
    http_srv_th.start()

    # add metrics
    my_metric_1 = Metric('my_metric_1', value=1, type=MetricType.gauge, comment='an amazing metric')
    my_metric_2 = Metric('my_metric_2', value=2, type=MetricType.gauge, comment='another amazing metric')

    # share this metrics with http server
    MetSrvShare.add(my_metric_1)
    MetSrvShare.add(my_metric_2)

    # main loop
    while True:
        my_metric_1.value = time.time()
        my_metric_2.value = 42
        time.sleep(1.0)

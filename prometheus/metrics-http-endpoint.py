#!/usr/bin/env python3

"""Prometheus HTTP endpoint template."""

from enum import Enum
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
from random import uniform
import re
import socket
from threading import Thread, Lock
from typing import Any
import time


class MetricType(Enum):
    """Definition of metric types."""
    COUNTER = 'counter'
    GAUGE = 'gauge'
    HISTOGRAM = 'histogram'
    SUMMARY = 'summary'
    UNTYPED = 'untyped'


class HistogramValue:
    """A class to store Histogram metric values."""

    def __init__(self, buckets: dict = None, _sum: float = 0.0):
        # private
        self._th_lock = Lock()
        self._buckets_d = {float('+inf'): 0}
        # process args
        if buckets is not None:
            self.update(buckets)
        self._sum = _sum

    @property
    def count(self):
        """Histogram sample count."""
        return self._buckets_d[float('+inf')]

    @count.setter
    def count(self, value):
        self._buckets_d[float('+inf')] = value

    @property
    def sum(self):
        """Histogram sample sum."""
        return self._sum

    @sum.setter
    def sum(self, value):
        self._sum = value

    def update(self, buckets: dict):
        """Update Histogram buckets values."""
        self._buckets_d.update(buckets)

    def clear(self):
        """Clear Histogram values."""
        self._buckets_d = {float('+inf'): 0}
        self.sum = 0


class Metric:
    """A Prometheus Metric."""

    def __init__(self, name: str, _type: MetricType = MetricType.UNTYPED, comment: str = ''):
        # arg metric name: name
        if re.fullmatch(r'[a-zA-Z_:][a-zA-Z\d_:]*', name):
            self._name = name
        else:
            raise ValueError(f'"{name}" is not a valid metric name')
        # arg metric type: type
        if type(_type) is MetricType:
            self._type = _type
        else:
            raise ValueError('type is of the wrong type (not a MetricType)')
        # arg metric comment: comment
        self.comment = str(comment)
        # private vars
        self._th_lock = Lock()
        self._values_d = dict()

    @property
    def name(self) -> str:
        """Name of metric (read-only property)."""
        return self._name

    @property
    def type(self) -> MetricType:
        """Type of metric (read-only property)."""
        return self._type

    def set(self, value: Any, labels: dict = None, timestamp: int = None):
        """Set a value for the metric with labels set in a dict.
        We can remove it if value it set to None.
        """
        # labels arg
        if labels is None:
            labels = dict()
        # check value type
        if value is not None:
            if self._type is MetricType.HISTOGRAM and type(value) is not HistogramValue:
                raise ValueError('value arg must be an HistogramValue for this type of metric.')
            # elif self._type is MetricType.SUMMARY and type(value) is not SummaryValue:
            #    raise ValueError('value arg must be a SummaryValue for this type of metric.')
            elif type(value) not in [int, float]:
                raise ValueError('value arg must be an int or float for this type of metric.')
        # build dict key labels_str
        # "label_name1=label_value1,label_name2=label_value2,[...]"
        labels_str = ''
        for label_name, label_value in labels.items():
            # add comma before next block
            if labels_str:
                labels_str += ','
            # apply escapes to label_value
            for rep_args in [('\\', '\\\\'), ('\n', '\\n'), ('"', '\\"')]:
                label_value = str(label_value).replace(*rep_args)
            # format label_str
            labels_str += f'{label_name}="{label_value}"'
        # add/update or remove the value in the values dict
        with self._th_lock:
            if value is None:
                self._values_d.pop(labels_str, None)
            else:
                self._values_d[labels_str] = (value, timestamp)

    def as_text(self) -> str:
        """Format the metric as Prometheus exposition format text."""
        txt = ''
        with self._th_lock:
            # if any value exists, format an exposition message
            if self._values_d:
                # add a comment line if defined
                if self.comment:
                    # apply escapes to comment
                    esc_comment = str(self.comment)
                    for rep_args in [('\\', '\\\\'), ('\n', '\\n')]:
                        esc_comment = esc_comment.replace(*rep_args)
                    txt += f'# HELP {self.name} {esc_comment}\n'
                # add a type line if defined
                if self.type is not MetricType.UNTYPED:
                    txt += f'# TYPE {self.name} {self.type.value}\n'
                # add every "name{labels} value [timestamp]" for the metric
                for labels, (value, timestamp) in self._values_d.items():
                    if labels:
                        txt += f'{self.name}{{{labels}}} {value}'
                    else:
                        txt += f'{self.name} {value}'
                    # optional timestamp
                    if timestamp is None:
                        txt += '\n'
                    else:
                        txt += f' {timestamp}\n'
        return txt


class MetricsHttpSrv:
    """A multi-threaded HTTP server for shares metrics with Prometheus."""

    class HandleRequests(BaseHTTPRequestHandler):
        """Custom HTTP handler"""

        def version_string(self) -> str:
            """Replace default server banner."""
            return 'self-service here ;-)'

        def log_message(self, format: str, *args: Any) -> None:
            """Replace log_message to turn off log msg."""
            return None

        def do_GET(self):
            """Process HTTP GET request."""
            # catch socket errors
            try:
                # for prometheus scrap endpoint
                if self.path == '/metrics':
                    # headers
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    # body
                    self.wfile.write(self.server.metrics_srv.as_text().encode('utf-8'))
                # on other path, nothing for you here
                else:
                    # return HTTP 404 page not found
                    self.send_response(404)
                    self.end_headers()
            except socket.error:
                pass

    @property
    def is_run(self):
        """Check if server currently processing requests."""
        return self._http_srv_run

    def __init__(self, port: int = 8080, bind: str = 'localhost'):
        # public
        self.port = port
        self.bind = bind
        # private
        self._th_lock = Lock()
        self._metrics_l = list()
        self._http_srv = None
        self._http_srv_th = None
        self._http_srv_run = False

    def add(self, metric: Metric):
        """Add metric to server share list."""
        with self._th_lock:
            self._metrics_l.append(metric)

    def remove(self, metric: Metric):
        """Remove metric from server share list."""
        with self._th_lock:
            self._metrics_l.remove(metric)

    def as_text(self) -> str:
        """Export metrics as Prometheus scrap file."""
        txt = ''
        with self._th_lock:
            for metric in self._metrics_l:
                txt += metric.as_text()
        return txt

    def start(self):
        """Start HTTP server as a thread."""
        # autodetect IPv6 address
        try:
            ipv6 = ip_address(self.bind).version == 6
        except ValueError:
            ipv6 = False
        # add IPv6 support to ThreadingHTTPServer if needed
        if ipv6:
            ThreadingHTTPServer.address_family = socket.AF_INET6
        #  init HTTP server
        ThreadingHTTPServer.allow_reuse_address = True
        self._http_srv = ThreadingHTTPServer((self.bind, self.port), self.HandleRequests)
        # pass metrics_srv to HandleRequests (available at HandleRequests.server.metrics_server)
        self._http_srv.metrics_srv = self
        # start server in a separate thread
        self._http_srv_th = Thread(target=self._http_srv.serve_forever, daemon=True)
        self._http_srv_th.start()

    def stop(self):
        """Stop HTTP server thread."""
        self._http_srv.shutdown()
        self._http_srv.server_close()


if __name__ == '__main__':
    # start HTTP server
    metrics_srv = MetricsHttpSrv()
    metrics_srv.start()

    # add metrics
    my_metric_gauge = Metric('my_metric_gauge', _type=MetricType.GAUGE, comment='an amazing gauge metric')
    my_metric_counter = Metric('my_metric_counter', _type=MetricType.COUNTER, comment='an amazing counter metric')

    # share this metrics with http server
    metrics_srv.add(my_metric_gauge)
    metrics_srv.add(my_metric_counter)

    # main loop
    loop_count = 0
    while True:
        loop_count += 1
        my_metric_gauge.set(42.0, labels={'foo': 'const'})
        my_metric_gauge.set(round(uniform(0, 100), 1), labels={'foo': 'rand'})
        my_metric_counter.set(loop_count, labels={'foo': 'loop'})
        time.sleep(1.0)

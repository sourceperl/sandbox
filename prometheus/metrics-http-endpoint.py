#!/usr/bin/env python3

"""Prometheus HTTP endpoint template."""

from enum import Enum
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from random import randint
import socket
from threading import Thread, Lock
from typing import Any
import time


class MetricType(Enum):
    """Definition of metric types."""
    COUNTER = 'counter'
    GAUGE = 'gauge'
    HISTORGRAM = 'histogram'
    SUMMARY = 'summary'
    UNTYPED = 'untyped'


class Metric:
    """A Prometheus Metric."""

    def __init__(self, name: str, m_type: MetricType = MetricType.UNTYPED, comment: str = ''):
        # private vars
        self._name = name
        self._m_type = m_type
        self._comment = None
        self._th_lock = Lock()
        self._values_d = dict()
        # public properties
        self.comment = comment

    @property
    def name(self) -> str:
        """Name of metric (read-only property)."""
        return self._name

    @property
    def m_type(self) -> MetricType:
        """Type of metric (read-only property)."""
        return self._m_type

    @property
    def comment(self) -> str:
        """Comment line for the metric."""
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value

    def set(self, value, labels: dict = None, timestamp: int = None):
        """Set a value for the metric with labels set in a dict.
        We can remove it if value it set to None.
        """
        # labels arg
        if labels is None:
            labels = dict()
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
                if self.m_type is not MetricType.UNTYPED:
                    txt += f'# TYPE {self.name} {self.m_type.value}\n'
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


class SrvMetricsList:
    """A thread safe list for shares metrics with HTTP server."""
    # private
    _th_lock = Lock()
    _metrics_l = list()

    @classmethod
    def add(cls, metric: Metric):
        """Add metric to server share list."""
        with cls._th_lock:
            cls._metrics_l.append(metric)

    @classmethod
    def remove(cls, metric: Metric):
        """Remove metric from server share list."""
        with cls._th_lock:
            cls._metrics_l.remove(metric)

    @classmethod
    def as_text(cls) -> str:
        """Export metrics as Prometheus scrap file."""
        txt = ''
        with cls._th_lock:
            for metric in cls._metrics_l:
                txt += metric.as_text()
        return txt


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
                self.wfile.write(SrvMetricsList.as_text().encode('utf-8'))
            # on other path, nothing for you here
            else:
                # return HTTP 404 page not found
                self.send_response(404)
                self.end_headers()
        except socket.error:
            pass


if __name__ == '__main__':
    # start HTTP server as a thread
    http_srv = ThreadingHTTPServer(('0.0.0.0', 8080), HandleRequests)
    http_srv_th = Thread(target=http_srv.serve_forever, daemon=True)
    http_srv_th.start()

    # add metrics
    my_metric_1 = Metric('my_metric_1', m_type=MetricType.GAUGE, comment='an amazing metric')
    my_metric_2 = Metric('my_metric_2', m_type=MetricType.GAUGE, comment='another amazing metric')

    # share this metrics with http server
    SrvMetricsList.add(my_metric_1)
    SrvMetricsList.add(my_metric_2)

    # main loop
    while True:
        my_metric_1.set(42, labels=dict(foo='the meaning of life'))
        my_metric_2.set(randint(0, 100), labels=dict(foo='random'))
        time.sleep(5.0)

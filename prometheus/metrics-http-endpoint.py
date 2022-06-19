#!/usr/bin/env python3

"""Prometheus HTTP endpoint template."""

from enum import Enum
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
from random import random
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

    def set(self, value: Any, labels_d: dict = None, timestamp: int = None):
        """Set a value for the metric with labels set in a dict.
        We can remove it if value it set to None.
        """
        # labels arg
        if labels_d is None:
            labels_d = dict()
        # if value is set, check its type
        if value is not None:
            if self._type is MetricType.HISTOGRAM or self._type is MetricType.SUMMARY:
                if type(value) is not dict:
                    raise ValueError('value arg must be a dict for this type of metric.')
            elif type(value) not in [int, float]:
                raise ValueError('value arg must be an int or float for this type of metric.')
        # build dict key labels_str
        # "label_name1=label_value1,label_name2=label_value2,[...]"
        labels_str = self.labels_d2str(labels_d)
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
                for lbl_id_str, (lbl_content, timestamp) in self._values_d.items():
                    if self._type is MetricType.HISTOGRAM:
                        txt += self._data2txt_histogram(lbl_id_str, lbl_content)
                    elif self._type is MetricType.SUMMARY:
                        txt += self._data2txt_summary(lbl_id_str, lbl_content)
                    else:
                        txt += self._data2txt_default(lbl_id_str, lbl_content, timestamp)
        return txt

    def _data2txt_histogram(self, lbl_id_str: str, lbl_content: dict) -> str:
        try:
            txt = ''
            # search for required keys in dict value
            b_count = lbl_content['count']
            b_sum = lbl_content['sum']
            # extract bucket float values
            buckets_l = list()
            # harvest float key, skip others
            for k, v in lbl_content.items():
                try:
                    # non-float raise ValueError
                    float(k)
                    buckets_l.append((k, v))
                except ValueError:
                    pass
            # set alpha order, with le="+Inf" at end
            buckets_l = sorted(buckets_l)
            buckets_l.append(('+Inf', b_count))
            # add buckets lines
            for b_item, b_value in buckets_l:
                lbl_id_str_bck = self.labels_d2str({'le': b_item}, _from=lbl_id_str)
                txt += f'{self.name}_bucket{self.lbl_f(lbl_id_str_bck)} {b_value}\n'
            # add sum line
            txt += f'{self.name}_sum{self.lbl_f(lbl_id_str)} {b_sum}\n'
            # add count line
            txt += f'{self.name}_count{self.lbl_f(lbl_id_str)} {b_count}\n'
            return txt
        except (IndexError, KeyError) as e:
            # TODO after debug set "pass" here
            print(e)
            return ''

    def _data2txt_summary(self, lbl_id_str: str, lbl_content: dict) -> str:
        try:
            txt = ''
            # search for required keys in dict value
            b_count = lbl_content['count']
            b_sum = lbl_content['sum']
            # extract bucket float values
            buckets_l = list()
            # harvest float key, skip others
            for k, v in lbl_content.items():
                try:
                    # non-float raise ValueError
                    float(k)
                    buckets_l.append((k, v))
                except ValueError:
                    pass
            # set alpha order
            buckets_l = sorted(buckets_l)
            # add buckets lines
            for b_item, b_value in buckets_l:
                lbl_str_bck = self.labels_d2str({'quantile': b_item}, _from=lbl_id_str)
                txt += f'{self.name}{self.lbl_f(lbl_str_bck)} {b_value}\n'
            # add sum line
            txt += f'{self.name}_sum{self.lbl_f(lbl_id_str)} {b_sum}\n'
            # add count line
            txt += f'{self.name}_count{self.lbl_f(lbl_id_str)} {b_count}\n'
            return txt
        except (IndexError, KeyError) as e:
            # TODO after debug set "pass" here
            print(e)
            return ''

    def _data2txt_default(self, lbl_id_str: str, lbl_content: Any, timestamp: int) -> str:
        txt = f'{self.name}{self.lbl_f(lbl_id_str)} {lbl_content}'
        # optional timestamp
        txt += f' {timestamp}\n' if timestamp else '\n'
        return txt

    @staticmethod
    def labels_d2str(lbl_d: dict, _from: str = ''):
        """"Convert labels dict {} to str "lbl_name1=lbl_val1,lbl_name2=lbl_val2,[...]".
        Can add convert to an already convert, initial str.
        """
        lbl_str = _from
        for lbl_name, lbl_val in lbl_d.items():
            # check label name
            if not re.fullmatch(r'[a-zA-Z_]\w*', lbl_name):
                raise ValueError(f'"{lbl_name}" is not a valid label name')
            # add comma before next block
            if lbl_str:
                lbl_str += ','
            # apply escapes to label_value
            for rep_args in [('\\', '\\\\'), ('\n', '\\n'), ('"', '\\"')]:
                lbl_val = str(lbl_val).replace(*rep_args)
            # format label_str
            lbl_str += f'{lbl_name}="{lbl_val}"'
        return lbl_str

    @staticmethod
    def lbl_f(lbl_s: str):
        """Format label string for export file lines."""
        return f'{{{lbl_s}}}' if lbl_s else ''


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
    my_metric_ratio = Metric('my_metric_ratio', _type=MetricType.GAUGE, comment='a gauge metric')
    my_metric_total = Metric('my_metric_total', _type=MetricType.COUNTER, comment='a counter metric')
    my_metric_histo = Metric('my_metric_histo', _type=MetricType.HISTOGRAM, comment='an histo metric')
    my_metric_sumy = Metric('my_metric_sumy', _type=MetricType.SUMMARY, comment='a summary metric')

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

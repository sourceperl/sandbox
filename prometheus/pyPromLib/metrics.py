"""This module implement pyPromLib metrics class."""

import logging
import re
import time
from enum import Enum
from threading import Lock
from typing import Any, Optional

logger = logging.getLogger(__name__)


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

    def set(self, value: Any, labels_d: Optional[dict] = None, ts: Optional[float] = None, ttl: Optional[float] = None):
        """Set a value for the metric with labels set in a dict.
        timestamp
        We can remove it if value it set to None.
        """
        # labels arg
        if labels_d is None:
            labels_d = dict()
        # if value is set, check its type
        if value is not None:
            if self._type is MetricType.GAUGE:
                if type(value) not in [bool, int, float]:
                    raise ValueError('value arg must be bool, int or float for this type of metric.')
            elif self._type is MetricType.COUNTER:
                if type(value) not in [int, float]:
                    raise ValueError('value arg must be int or float for this type of metric.')
            elif self._type is MetricType.HISTOGRAM or self._type is MetricType.SUMMARY:
                if type(value) is not dict:
                    raise ValueError('value arg must be a dict for this type of metric.')
        # build dict key labels_str
        # "label_name1=label_value1,label_name2=label_value2,[...]"
        labels_str = self._labels_d2str(labels_d)
        # add/update or remove the value in the values dict
        with self._th_lock:
            if value is None:
                self._values_d.pop(labels_str, None)
            else:
                expire_at = (time.monotonic() + ttl) if ttl else None
                self._values_d[labels_str] = (value, ts, expire_at)

    def as_text(self) -> str:
        """Format the metric as Prometheus exposition format text."""
        txt = ''
        with self._th_lock:
            # purge expired value (reach ttl_s) from values dict
            purge_l = []
            for key, (_value, _timestamp_ms, expire_at) in self._values_d.items():
                if expire_at and time.monotonic() > expire_at:
                    purge_l.append(key)
            for rm_key in purge_l:
                self._values_d.pop(rm_key)
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
                for lbl_id_str, (value, ts, _expire_at) in self._values_d.items():
                    if self._type is MetricType.HISTOGRAM:
                        txt += self._data2txt_histogram(lbl_id_str, value)
                    elif self._type is MetricType.SUMMARY:
                        txt += self._data2txt_summary(lbl_id_str, value)
                    else:
                        txt += self._data2txt_default(lbl_id_str, value, ts)
        return txt

    def _data2txt_histogram(self, lbl_id_str: str, histo_d: dict) -> str:
        try:
            txt = ''
            # search for required keys in dict value
            b_count = histo_d['count']
            b_sum = histo_d['sum']
            # extract bucket float values
            buckets_l = list()
            # harvest float key, skip others
            for k, v in histo_d.items():
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
                lbl_id_str_bck = self._labels_d2str({'le': b_item}, _from=lbl_id_str)
                txt += f'{self.name}_bucket{self._lbl_f(lbl_id_str_bck)} {b_value}\n'
            # add sum line
            txt += f'{self.name}_sum{self._lbl_f(lbl_id_str)} {b_sum}\n'
            # add count line
            txt += f'{self.name}_count{self._lbl_f(lbl_id_str)} {b_count}\n'
            return txt
        except (IndexError, KeyError) as e:
            if e.__traceback__:
                logger.warning(f'except occur: {e!r} at line {e.__traceback__.tb_lineno}')
            return ''

    def _data2txt_summary(self, lbl_id_str: str, sum_d: dict) -> str:
        try:
            txt = ''
            # search for required keys in dict value
            b_count = sum_d['count']
            b_sum = sum_d['sum']
            # extract bucket float values
            buckets_l = list()
            # harvest float key, skip others
            for k, v in sum_d.items():
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
                lbl_str_bck = self._labels_d2str({'quantile': b_item}, _from=lbl_id_str)
                txt += f'{self.name}{self._lbl_f(lbl_str_bck)} {b_value}\n'
            # add sum line
            txt += f'{self.name}_sum{self._lbl_f(lbl_id_str)} {b_sum}\n'
            # add count line
            txt += f'{self.name}_count{self._lbl_f(lbl_id_str)} {b_count}\n'
            return txt
        except (IndexError, KeyError) as e:
            if e.__traceback__:
                logger.warning(f'except occur: {e!r} at line {e.__traceback__.tb_lineno}')
            return ''

    def _data2txt_default(self, lbl_id_str: str, value: Any, ts: int) -> str:
        # prometheus metrics file accept 0/1 not False/True
        if type(value) is bool:
            value = int(value)
        # init value line
        txt = f'{self.name}{self._lbl_f(lbl_id_str)} {value}'
        # optional timestamp at end of line
        txt += f' {round(ts * 1000)}\n' if ts else '\n'
        return txt

    @staticmethod
    def _labels_d2str(lbl_d: dict, _from: str = ''):
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
    def _lbl_f(lbl_s: str):
        """Format label string for export file lines."""
        return f'{{{lbl_s}}}' if lbl_s else ''

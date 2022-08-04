"""This module implement pyPromLib metrics class."""

from enum import Enum
import re
from threading import Lock
from typing import Any


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


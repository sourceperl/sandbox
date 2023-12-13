#!/usr/bin/env python3

""" Unit test of regex."""

import re
import unittest


class TestMetricRegex(unittest.TestCase):
    pattern = re.compile(r'(?!__.*)(?P<name>[a-zA-Z_:][a-zA-Z0-9_:]*)(?:{(?P<labels>.*?)})?')
    match_l = ['my_metric', 'my_metric{tag="foo"}', ]
    no_match_l = ['__my_metric', 'my_m$etric{}', ]

    def test_match(self):
        for test_str in self.match_l:
            self.assertTrue(self.pattern.fullmatch(test_str))

    def test_no_match(self):
        for test_str in self.no_match_l:
            self.assertFalse(self.pattern.fullmatch(test_str))


class TestLabelsRegex(unittest.TestCase):
    pattern = re.compile(r'(?:(?!__.*)[a-zA-Z_][a-zA-Z0-9_]*="[^"]*",?)+')
    match_l = ['tag="foo"', 'tag="foo",', 'truc="machin",bidule="42"', 'up="test",foo="value"']
    no_match_l = ['__tag="foo"', 'tag=foo,', 'tag="foo"""', 'tag="z",,']

    def test_match(self):
        for test_str in self.match_l:
            self.assertTrue(self.pattern.fullmatch(test_str))

    def test_no_match(self):
        for test_str in self.no_match_l:
            self.assertFalse(self.pattern.fullmatch(test_str))


if __name__ == '__main__':
    unittest.main()

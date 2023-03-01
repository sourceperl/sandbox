#!/usr/bin/env python3

"""Connect logging module to syslog."""

import logging
from logging import Formatter, StreamHandler
from logging.handlers import SysLogHandler
import sys


# some const
APP_NAME = 'to_syslog_test'


# add default handler (stderr)
def_hdl = StreamHandler()
def_hdl.setLevel(logging.DEBUG)
def_hdl.setFormatter(Formatter('%(asctime)s %(levelname)-8s %(message)s'))
handlers = [def_hdl]
# add syslog handler (append message to /var/log/syslog) on linux system
if sys.platform.startswith('linux'):
    syslog_hdl = SysLogHandler(address='/dev/log')
    syslog_hdl.setLevel(logging.INFO)
    syslog_hdl.setFormatter(Formatter(f'{APP_NAME}[%(process)d]: %(message)s'))
    handlers.append(syslog_hdl)
logging.basicConfig(level=logging.DEBUG, handlers=handlers)
logging.info('a test message')

#!/usr/bin/env python3

"""Connect logging module to syslog."""

import logging
from logging import StreamHandler
from logging.handlers import SysLogHandler


# some const
APP_NAME = 'to_syslog_test'


# add default handler (stderr) and syslog handler (append message to /var/log/syslog)
handlers = [StreamHandler(), SysLogHandler(address='/dev/log')]
logging.basicConfig(format=f'{APP_NAME}[%(process)d]: %(levelname)-8s %(message)s', level=logging.DEBUG, handlers=handlers)
logging.info('a test message')

#!/usr/bin/env python3

"""Basic test of topics subscribe with callback handler."""

import time
import socket
# sudo pip3 install paho-mqtt==1.6.1
from paho.mqtt import subscribe


def msg_handler(_client, _userdata, message):
    """Handle publish on MQTT subscribed messages. Manage published on subscribed topics"""
    print(f'{message.topic} = {message.payload}')


if __name__ == '__main__':
    while True:
        try:
            subscribe.callback(msg_handler, '/#', hostname='test.mosquitto.org')
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(2.0)

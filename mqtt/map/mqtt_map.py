#!/usr/bin/env python3

"""Produce a topics map of an MQTT broker."""

from textwrap import shorten
import time
from threading import Thread, Lock
# sudo pip3 install paho-mqtt==1.6.1
from paho.mqtt import subscribe


# some class
class MqttMapper:
    """MQTT mapper:
    an internal thread collect topics and helper functions permit to export the map.
    """

    def __init__(self, hostname: str, topics: str = '#'):
        # public
        self.hostname = hostname
        self.topics = topics
        # private
        self._lock = Lock()
        self._topics_d = dict()
        self._msg_count = 0
        # start internal topic collector thread
        self._collect_th = Thread(target=self._collect_th_main, daemon=True)
        self._collect_th.start()

    def _collect_th_main(self) -> None:
        """Collect thread task."""
        while True:
            try:
                subscribe.callback(self._on_mqtt_msg, hostname=self.hostname, topics=self.topics)
            except (ConnectionRefusedError, OSError):
                time.sleep(2.0)

    def _on_mqtt_msg(self, _client, _userdata, message) -> None:
        """Collect thread messages handler."""
        with self._lock:
            self._msg_count += 1
            # populate internal topics dict
            try:
                # limit size of payload to 120 chars
                self._topics_d[message.topic] = shorten(message.payload.decode(), width=120, placeholder='[...]')
            except UnicodeError:
                # non-UTF-8 payload mark as "[BLOB]"
                self._topics_d[message.topic] = '[BLOB]'

    def as_txt(self) -> str:
        """Export topics map as text."""
        txt = ''
        with self._lock:
            for topic in sorted(self._topics_d):
                payload = self._topics_d[topic]
                txt += f'{topic} -> {payload}\n'
        return txt

    @property
    def msg_counter(self):
        """MQTT messages counter."""
        with self._lock:
            return self._msg_count

    @property
    def topics_counter(self):
        """MQTT topics counter."""
        with self._lock:
            return len(self._topics_d)


if __name__ == '__main__':
    # start MQTT mapping
    mqtt_map = MqttMapper(hostname='mqtt.eclipseprojects.io')
    # let time for collect
    time.sleep(10.0)
    # export result
    print(mqtt_map.as_txt())

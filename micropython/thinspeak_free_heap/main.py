# Publish free heap to Thingspeak using MQTT
# use mycropython on an ESP8266 NodeMCU board

import network
from umqtt.robust import MQTTClient
import urandom
import sys
import time
import os
import gc

# some const
WIFI_SSID = "WIFI_XXXXX"
WIFI_PWD = "XXXXXXX"
TS_SRV = "mqtt.thingspeak.com"
TS_USER_ID = "XXXXXXXXXXXXXXXX"
TS_MQTT_API_KEY = "XXXXXXXXXXXXXXXX"
TS_CHANNEL_ID = "42"
TS_CHANNEL_W_API_KEY = "XXXXXXXXXXXXXXXX"
TS_PUBLISH_PERIOD = 30

# turn off access point interface (default is on)
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# turn on station interface (default is off) and connect to WIFI_SSID
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(WIFI_SSID, WIFI_PWD)

# wait for connection
t = 0
while True:
    if sta_if.isconnected():
        break
    print("try to connect to %s (%d)" % (WIFI_SSID, t))
    t += 1
    time.sleep(1.0)
print("connect to %s ok" % WIFI_SSID)

# connect to TS MQTT broker
client = MQTTClient(client_id="client_%s" % urandom.getrandbits(16),
                    server=TS_SRV,
                    user=TS_USER_ID,
                    password=TS_MQTT_API_KEY,
                    ssl=False)

while True:
    try:
        # connect to server
        client.connect()
        print("connect to server %s ok" % TS_SRV)

        # publish loop
        try:
            while True:
                topic = "channels/%s/publish/%s" % (TS_CHANNEL_ID, TS_CHANNEL_W_API_KEY)
                payload = "field1=%d" % gc.mem_free()
                client.publish(topic, payload)
                print("publish %s to %s" % (payload, topic))
                time.sleep(TS_PUBLISH_PERIOD)
        except Exception as e:
            sys.print_exception(e)

        # disconnect to server
        client.disconnect()
        print("disconnect from server %s" % TS_SRV)
    except Exception as e:
        sys.print_exception(e)
        time.sleep(TS_PUBLISH_PERIOD)

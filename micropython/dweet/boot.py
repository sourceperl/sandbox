import machine
import network
import pycom
import time

# some const
from private_wifi import WIFI_SSID, WIFI_PWD

# LED status is red
pycom.heartbeat(False)
pycom.rgbled(0x120000)

# wifi setup for pycom
wlan = network.WLAN(mode=network.WLAN.STA)
# scan available SSID
for net in wlan.scan():
    if net.ssid == WIFI_SSID:
        # LED status is yellow
        pycom.rgbled(0x121200)
        print("SSID %s found, connect to it" % WIFI_SSID)
        wlan.connect(net.ssid, auth=(net.sec, WIFI_PWD), timeout=5000)
        while not wlan.isconnected():
            # save power while waiting
            machine.idle()
        print("connection succeeded")
        break

# LED status is green
pycom.rgbled(0x001200)

# wifi setup for ESP8266
# # turn off access point interface (default is on)
# ap_if = network.WLAN(network.AP_IF)
# ap_if.active(False)
#
# # turn on station interface (default is off) and connect to WIFI_SSID
# sta_if = network.WLAN(network.STA_IF)
# sta_if.active(True)
# sta_if.connect(WIFI_SSID, WIFI_PWD)
#
# # wait for connection
# t = 0
# while True:
#     if sta_if.isconnected():
#         break
#     print("try to connect to %s (%d)" % (WIFI_SSID, t))
#     t += 1
#     time.sleep(1.0)
# print("connect to %s ok" % WIFI_SSID)

import machine
import network
import pycom

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

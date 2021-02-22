import gc
import time
import urequests
from machine import Pin
import network

# some const
from private import WIFI_SSID, WIFI_PWD, DWEET_ID
LED_GPIO = 16
PUBLISH_PERIOD = 15

# init
# connect to wifi
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PWD)
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())
# IOs init
led = Pin(LED_GPIO, Pin.OUT)
# vars init
life_count = 0

# main loop
while True:
    # format and publish message
    life_count += 1
    # try:
    # HTTP version
    headers = {'Content-Type': 'application/json'}
    r = urequests.post("http://dweet.io/dweet/for/%s" % DWEET_ID,
                       json=dict(life=life_count, mem=gc.mem_free()),
                       headers=headers)
    r.close()
    # wait for next loop (with periodic led blink as sign of life)
    for i in range(10):
        led.value(not led.value())
        time.sleep(PUBLISH_PERIOD/10)

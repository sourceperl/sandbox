import gc
import time
import urequests

# some const
from private_dweet import DW_UUID
PUBLISH_PERIOD = 15

# init
gc.enable()
i = 0

# main loop
while True:
    # format and publish message
    i += 1
    # try:
    # HTTP version
    r = urequests.post("http://dweet.io/dweet/for/%s" % DW_UUID, json=dict(life=i, mem=gc.mem_free()))
    r.close()
    # HTTPS version (need more memory)
    # r = urequests.post("https://dweet.io:443/dweet/for/%s" % DW_UUID, json=dict(life=i, mem=gc.mem_free()))
    # r.close()
    # except:
    #     pass
    # wait for next loop
    time.sleep(PUBLISH_PERIOD)

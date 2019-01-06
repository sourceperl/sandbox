# bbc micro:bit + robot kitronik :move

from microbit import *
import radio

# some const
M_RIGHT = pin1
M_LEFT = pin2
# reduce speed of a wheel
M_RIGHT_OFFSET = 10
M_LEFT_OFFSET = 0

# setup
radio.on()
#radio.config(group=0)
# IO for left and righ servos
M_RIGHT.set_analog_period(20)
M_LEFT.set_analog_period(20)

# main loop
while True:
    # emergency stop
    if button_a.was_pressed() or button_b.was_pressed():
        M_LEFT.write_analog(0)
        M_RIGHT.write_analog(0)
    # radio 
    msg = radio.receive()
    if msg:
        try:
            f,r = map(int, msg.split(","))
        except:
            pass
        # compute servos values
        srv_l = 90 + (90 * f/100) + (90 * r/100) - M_LEFT_OFFSET
        srv_r = 90 - (90 * f/100) + (90 * r/100) + M_RIGHT_OFFSET
        # cutoff (avoid servo stop)
        if srv_l < 1:
            srv_l = 1
        if srv_r < 1:
            srv_r = 1
        # force stop
        if f == 0 and r == 0:
            srv_l = 0
            srv_r = 0
        # apply
        M_LEFT.write_analog(srv_l)
        M_RIGHT.write_analog(srv_r)
        print("f = %s / r = %s" %(f,r))
        print("srv_l = %s / srv_r = %s" %(srv_l, srv_r))

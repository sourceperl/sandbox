# bbc micro:bit + bit:commander (4tronix)
# use joystick to command robot kitronik :move

from microbit import *
import radio

# setup
radio.on()
#radio.config(group=0)
s_forward, s_right = 0, 0

# main loop
while True:
    # read joystick and scale it 
    # -100 is full reverse forward / 0 is stop / +100% is full forward 
    forward = round(200 * pin2.read_analog()/1023) - 100
    right = round(200 * pin1.read_analog()/1023) - 100
    # add a cutoff
    if abs(forward) < 20:
        forward = 0
    if abs(right) < 20:
        right = 0
    # send values on change
    if (s_forward, s_right) != (forward, right):
        (s_forward, s_right) = (forward, right)
        print("forward=%s right=%s" % (forward, right))
        radio.send("%i,%i" % (forward, right))
    # red button send stop command
    if pin12.read_digital():
        radio.send("0,0")
    sleep(50)

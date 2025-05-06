import time

from PLCToolbox.timers import TimerOffDelay, TimerOnDelay, TimerPeriod

# Timer off-delay
print('#'*10 + ' TimerOffDelay ' + '#'*10)
my_toff = TimerOffDelay(preset_ms=4_000)
my_toff.input = True
print(my_toff)
time.sleep(.5)
my_toff.input = False
while my_toff.output:
    print(my_toff)
    time.sleep(1.0)
print(my_toff)
my_toff.input = True
print(my_toff)
my_toff.input = False
while my_toff.output:
    print(my_toff)
    time.sleep(1.0)
print(my_toff)
print()


# Timer on-delay
print('#'*10 + ' TimerOnDelay ' + '#'*10)
my_ton = TimerOnDelay(preset_ms=4_000)
my_ton.input = True
while not my_ton.output:
    print(my_ton)
    time.sleep(1.0)
print(my_ton)

"""
A very basic example for remote debuging on a RevPi Connect 4 with a DIO board.

Before using this, follow these steps:
    # on revpi cmd line
    # turn on PLC server by setting "plcserver = 1"
    sudo vim /etc/revpipyload/revpipyload.conf 
    # add <ip_address>,2 to PLC server acl
    sudo vim /etc/revpipyload/aclplcserver.conf
    # restart revpipyload
    sudo systemctl restart revpipyload.service
"""

from private_data import PLC_ADDRESS

# pip install revpimodio2
from revpimodio2 import BLUE, GREEN, OFF, RED, RISING, Cycletools, run_net_plc


class Main:
    def __init__(self) -> None:
        # main vars
        self.counter = 0
        self.i = 0

    def __call__(self, cycle: Cycletools) -> None:
        """RevPiModIO will call this function every 50 milliseconds."""

        # on first cycle
        if cycle.first:
            self.counter = 0
            cycle.core.A1 = OFF
            cycle.core.A2 = OFF
            cycle.core.A3 = OFF
            cycle.core.A4 = OFF
            cycle.core.A5 = OFF

        # on program exit
        if cycle.last:
            cycle.core.A1 = OFF
            cycle.core.A2 = OFF
            cycle.core.A3 = OFF
            cycle.core.A4 = OFF
            cycle.core.A5 = OFF
            print('end of program')

        # health of program: flashing some leds
        cycle.core.A3 = GREEN if cycle.flag1c else OFF
        cycle.core.A4 = BLUE if cycle.flag5c else OFF
        cycle.core.A5 = RED if cycle.flag10c else OFF

        # compares the state of I_1 with the last cycle
        if cycle.changed(cycle.io.I_1, edge=RISING):
            self.counter += 1
            cycle.core.a1blue(not cycle.core.a1blue())

        # debug message
        self.i += 1
        print(f'cycle #{self.i} flag10c = {cycle.flag10c}')


# run main with a cycle set to 50ms (default)
run_net_plc(address=PLC_ADDRESS, func=Main(), cycletime=50)

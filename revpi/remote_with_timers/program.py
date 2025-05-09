from private_data import PLC_ADDRESS
from revpimodio2 import Cycletools, RevPiNetIO
from revpimodio2.io import IOBase
from PLCToolbox.timers import TimerOnDelay, TimerOffDelay


class App:
    def __init__(self) -> None:
        # init RevPi IO
        self.rp_io = RevPiNetIO(PLC_ADDRESS, autorefresh=True)
        self.rp_io.handlesignalend(self.exit)
        # init timers
        self.ton_btn1 = TimerOnDelay(preset_ms=1_000)
        self.tof_btn1 = TimerOffDelay(preset_ms=5_000)
        self.ton_rel2 = TimerOnDelay(preset_ms=2_000)
        # IO objects: abstract logical (relay 1) vs physical access path (O_1)
        self.relay_1: IOBase = getattr(self.rp_io.io, 'O_1')
        self.relay_2: IOBase = getattr(self.rp_io.io, 'O_2')
        self.relay_3: IOBase = getattr(self.rp_io.io, 'O_3')
        self.btn_1: IOBase = getattr(self.rp_io.io, 'I_1')

    def __call__(self):
        self.rp_io.cycleloop(self._cycleloop, cycletime=50)
    
    def _cycleloop(self, cycle: Cycletools):
        if cycle.first:
            self.init()
        self.loop(cycle)

    def init(self):
        self.relay_1.value = True

    def exit(self):
        self.relay_1.value = False
        self.relay_2.value = False
        self.relay_3.value = False

    def loop(self, cycle: Cycletools):
        self.relay_2(self.tof_btn1(self.ton_btn1(not self.btn_1.value)))
        self.relay_3.value = self.ton_rel2(self.relay_2.value)


app = App()
app()

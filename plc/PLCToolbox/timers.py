import time


def monotonic_ms() -> int:
    """Return the value (in milliseconds) of a monotonic clock."""
    return round(time.monotonic() * 1000)


class TimerOffDelay:
    def __init__(self, preset_ms: int) -> None:
        # public
        self.preset_ms = preset_ms
        # private
        self._in = False
        self._start_time = monotonic_ms()

    @property
    def elapsed_ms(self) -> int:
        if not self._in:
            return monotonic_ms() - self._start_time
        else:
            return 0

    @property
    def input(self) -> bool:
        return self._in

    @input.setter
    def input(self, value: bool):
        # on falling edge (True -> False)
        if self._in and not value:
            self._start_time = monotonic_ms()
        self._in = value

    @property
    def output(self) -> bool:
        if self._in:
            return True
        else:
            return self.elapsed_ms < self.preset_ms

    def __str__(self) -> str:
        return f'TimerOffDelay(preset_ms={self.preset_ms}, elapsed_ms={self.elapsed_ms}, ' \
               f'input={self.input}, output={self.output})'


class TimerOnDelay:
    def __init__(self, preset_ms: int) -> None:
        # public
        self.preset_ms = preset_ms
        # private
        self._in = False
        self._start_time = monotonic_ms()

    @property
    def elapsed_ms(self) -> int:
        if self._in:
            return monotonic_ms() - self._start_time
        else:
            return 0

    @property
    def input(self) -> bool:
        return self._in

    @input.setter
    def input(self, value: bool):
        # on rising edge (False -> True)
        if not self._in and value:
            self._start_time = monotonic_ms()
        self._in = value

    @property
    def output(self) -> bool:
        if self._in:
            return self.elapsed_ms >= self.preset_ms
        else:
            return False

    def __str__(self) -> str:
        return f'TimerOnDelay(preset_ms={self.preset_ms}, elapsed_ms={self.elapsed_ms}, ' \
               f'input={self.input}, output={self.output})'


class TimerPeriod:
    def __init__(self, preset_ms: int, resettable: bool = False) -> None:
        # public
        self.preset_ms = preset_ms
        self.resettable = resettable
        # private
        self._in = False
        self._pulse_generated = False
        self._start_time = monotonic_ms()

    @property
    def elapsed_ms(self) -> int:
        if not self._pulse_generated:
            return 0
        return min(monotonic_ms() - self._start_time, self.preset_ms)

    @property
    def input(self) -> bool:
        return self._in

    @input.setter
    def input(self, value: bool):
        # on rising edge (False -> True)
        if not self._in and value:
            if self._pulse_generated:
                if self.resettable:
                    self._start_time = monotonic_ms()
            else:
                self._pulse_generated = True
                self._start_time = monotonic_ms()
        # on falling edge (True -> False)
        if self._in and not value:
            if not self.output:
                self._pulse_generated = False
        # set input state
        self._in = value

    @property
    def output(self) -> bool:
        if self._pulse_generated:
            return self.elapsed_ms < self.preset_ms
        else:
            return False

    def __str__(self) -> str:
        return f'TimerPeriod(preset_ms={self.preset_ms}, elapsed_ms={self.elapsed_ms}, ' \
               f'input={self.input}, output={self.output})'

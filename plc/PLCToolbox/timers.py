import time
from typing import Optional


def monotonic_ms() -> int:
    """Return the value (in milliseconds) of a monotonic clock."""
    return int(time.monotonic() * 1000)


class TimerOffDelay:
    def __init__(self, preset_ms: int) -> None:
        # public
        self.preset_ms = preset_ms
        # private
        self._in = False
        self._start_ms: Optional[int] = None

    def __str__(self) -> str:
        return f'TimerOffDelay(preset_ms={self.preset_ms}, elapsed_ms={self.elapsed_ms}, ' \
               f'input={self.input}, output={self.output})'

    def __call__(self, input: bool) -> bool:
        self.input = input
        return self.output

    @property
    def elapsed_ms(self) -> int:
        if self._start_ms is None:
            return 0
        return min(self.preset_ms, monotonic_ms() - self._start_ms)

    @property
    def input(self) -> bool:
        return self._in

    @input.setter
    def input(self, value: bool):
        # on rising edge (False -> True)
        if not self._in and value:
            self._start_ms = None
        # on falling edge (True -> False)
        if self._in and not value:
            self._start_ms = monotonic_ms()
        self._in = value

    @property
    def output(self) -> bool:
        if not self.preset_ms or self._start_ms is None:
            return self._in
        else:
            return self.elapsed_ms < self.preset_ms


class TimerOnDelay:
    def __init__(self, preset_ms: int) -> None:
        # public
        self.preset_ms = preset_ms
        # private
        self._in = False
        self._start_ms: Optional[int] = None

    def __str__(self) -> str:
        return f'TimerOnDelay(preset_ms={self.preset_ms}, elapsed_ms={self.elapsed_ms}, ' \
               f'input={self.input}, output={self.output})'

    def __call__(self, input: bool) -> bool:
        self.input = input
        return self.output

    @property
    def elapsed_ms(self) -> int:
        if self._start_ms is None:
            return 0
        return min(self.preset_ms, monotonic_ms() - self._start_ms)

    @property
    def input(self) -> bool:
        return self._in

    @input.setter
    def input(self, value: bool):
        # on rising edge (False -> True)
        if not self._in and value:
            self._start_ms = monotonic_ms()
        # on falling edge (True -> False)
        if self._in and not value:
            self._start_ms = None
        self._in = value

    @property
    def output(self) -> bool:
        if not self.preset_ms:
            return self._in
        return self.elapsed_ms >= self.preset_ms


class TimerPeriod:
    def __init__(self, preset_ms: int, resettable: bool = False) -> None:
        # public
        self.preset_ms = preset_ms
        self.resettable = resettable
        # private
        self._in = False
        self._start_ms: Optional[int] = None

    def __str__(self) -> str:
        return f'TimerPeriod(preset_ms={self.preset_ms}, elapsed_ms={self.elapsed_ms}, ' \
               f'input={self.input}, output={self.output})'

    def __call__(self, input: bool) -> bool:
        self.input = input
        return self.output

    @property
    def elapsed_ms(self) -> int:
        if not self._start_ms:
            return 0
        return min(monotonic_ms() - self._start_ms, self.preset_ms)

    @property
    def input(self) -> bool:
        return self._in

    @input.setter
    def input(self, value: bool):
        # on rising edge (False -> True)
        if not self._in and value:
            if self._start_ms is None or self.resettable:
                self._start_ms = monotonic_ms()
        # on falling edge (True -> False)
        if self._in and not value:
            if self.elapsed_ms >= self.preset_ms:
                self._start_ms = None
        # set input state
        self._in = value

    @property
    def output(self) -> bool:
        if self._start_ms is None:
            return False
        if not self._in and self.elapsed_ms >= self.preset_ms:
            self._start_ms = None
            return False
        else:
            return self.elapsed_ms < self.preset_ms

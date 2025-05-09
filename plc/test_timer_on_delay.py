import time
from dataclasses import dataclass, field
from typing import List

import matplotlib.pyplot as plt
from PLCToolbox.timers import TimerOnDelay


@dataclass
class Signal:
    name: str
    data: list = field(default_factory=list)


input_sig = Signal('input')
output_sig = Signal('output')
elapsed_ms_sig = Signal('elapsed_ms')
preset_ms_sig = Signal('preset_ms')
time_line = []

# Timer on-delay
test_pattern = [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, ] 
ton = TimerOnDelay(preset_ms=5)
t_origin = time.monotonic()

for idx, value in enumerate(test_pattern):
    # add 4 x 250 us points for each ms
    for _ in range(4):
        input = bool(value)
        output = ton(input)
        input_sig.data.append(input)
        output_sig.data.append(output)
        elapsed_ms_sig.data.append(ton.elapsed_ms)
        preset_ms_sig.data.append(ton.preset_ms)
        time_line.append(round((time.monotonic() - t_origin) * 1_000, 1))
        time.sleep(0.25e-3)

# define the signals
signals: List[Signal] = [input_sig, output_sig, elapsed_ms_sig, preset_ms_sig]

# Create a figure with three subplots
fig, axs = plt.subplots(len(signals), 1, figsize=(10, 6), sharex=True)

# Plot each signal on a separate subplot
for i, signal in enumerate(signals):
    ax = axs[i]
    ax.set_ylabel(signal.name)
    ax.step(time_line, signal.data, where='pre')
    ax.grid()

# set x-axis label for the last subplot
axs[-1].set_xlabel('Time (ms)')

# set title for the entire figure
fig.suptitle('Digital Timing Diagram of TON timer')

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()

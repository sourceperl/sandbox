import time
from dataclasses import dataclass, field
from typing import List

import matplotlib.pyplot as plt
from PLCToolbox.timers import TimerPeriod


@dataclass
class Signal:
    name: str
    data: list = field(default_factory=list)


input_sig = Signal('input')
output_sig = Signal('output')
elapsed_ms_sig = Signal('elapsed_ms')
preset_ms_sig = Signal('preset_ms')

# Timer on-delay
test_pattern = [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, ]
tp = TimerPeriod(preset_ms=4)

for idx, value in enumerate(test_pattern):
    input = bool(value)
    output = tp(input)
    input_sig.data.append(input)
    output_sig.data.append(output)
    elapsed_ms_sig.data.append(tp.elapsed_ms)
    preset_ms_sig.data.append(tp.preset_ms)
    time.sleep(1e-3)

# define the signals
signals: List[Signal] = [input_sig, output_sig, elapsed_ms_sig, preset_ms_sig]

# Create a figure with three subplots
fig, axs = plt.subplots(len(signals), 1, figsize=(10, 6), sharex=True)

# Plot each signal on a separate subplot
for i, signal in enumerate(signals):
    ax = axs[i]
    ax.set_ylabel(signal.name)
    ax.step(range(len(signal.data)), signal.data, where='pre')
    ax.grid()

# set x-axis label for the last subplot
axs[-1].set_xlabel('Time (ms)')

# set title for the entire figure
fig.suptitle('Digital Timing Diagram of TP timer')

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()

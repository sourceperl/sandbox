import matplotlib.pyplot as plt
import numpy as np

# some const
V0 = 1
R = 1000
C = 0.001

# compute
tau = R * C
t = np.linspace(start=0, stop=5 * tau, num=500)
vc = V0 * (1 - np.exp(-t / tau))

# plot
plt.figure(figsize=(10, 6))
plt.plot(t, vc, label='Voltage across the capacitor', color='blue')
plt.axhline(y=V0, color='r', linestyle='--', label='Applied voltage (V0)')
plt.title('Charging curve of a capacitor through a resistor')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True)
plt.show()

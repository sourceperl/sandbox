import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 300, 1_000)
y = (1+1/x)**x

plt.axhline(np.e, color='r', linestyle='--', label='$e$')
plt.plot(x, y, label=r'$(1+\frac{1}{n})^n$')
plt.grid()
plt.legend()
plt.show()

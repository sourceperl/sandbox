import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

# a=8, b=2
x = np.arange(0, 1, 0.001)
y = beta.pdf(x, a=8, b=2)
plt.plot(x, y, color='lightcoral', linestyle='--', label='a=8, b=2')

# a=80, b=20
x = np.arange(0, 1, 0.001)
y = beta.pdf(x, a=80, b=20)
plt.plot(x, y, color='firebrick', label='a=80, b=20')

plt.grid()
plt.xlabel('p')
plt.ylabel('PDF(p)')
plt.legend()
plt.show()

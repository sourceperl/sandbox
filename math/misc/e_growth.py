"""
Comparison of two methods of calculating the growth of an initial capital of 100 units, based on a growth rate r and 
a period t.

The graph shows how the final value calculated by compounding approaches that calculated by continuous exponential 
growth as t increases.
"""

import matplotlib.pyplot as plt
import numpy as np

r = 0.02
t = np.linspace(1, 250, 250)

y_cont = 100 * np.exp(r)
y_comp = 100 * (1 + (r/t))**t

plt.axhline(y_cont, linestyle='--', color='orange', label='$100 * e^{r}$')
plt.plot(t, y_comp, label=r'$100 * (1+\frac{r}{t})^t$')
plt.title(f'for r = {r}')
plt.xlabel('t')
plt.ylabel('value')
plt.legend()
plt.grid()
plt.show()

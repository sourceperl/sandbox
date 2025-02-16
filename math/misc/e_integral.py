from math import e
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np


def f_x(x: float) -> float:
    return 1/x


def approx_integral(func: Callable, start: float, stop: float, n_steps: int = 1_000) -> float:
    dx = (stop-start)/n_steps
    integral = 0.5 * (func(start) + func(stop)) * dx

    for i in range(1, n_steps):
        x_i = start + i * dx
        integral += func(x_i) * dx

    return integral


result = approx_integral(f_x, start=1, stop=e, n_steps=1_000)
print(f'result (approx at 6 digits after .) = {round(result, 6)}')

xa, xb = 1.0, e
x = np.linspace(0.5, 5, 1000)
y = np.vectorize(f_x)(x)

plt.plot(x, y)
plt.title(r'The area under the hyperbola $\frac{1}{x}$ is equal to 1 on the interval [1, e].', fontsize=9)
plt.fill_between(x, y, where=(x >= xa) & (x <= xb), color='skyblue', alpha=0.4)
plt.axvline(xa, color='orange', ls='--')
plt.axvline(xb, color='orange', ls='--')
plt.text(1.75, 0.25, f'$\\int_{{1}}^{{e}} \\frac{{1}}{{x}} \\, dx = {result:.02f}$',
         horizontalalignment='center', fontsize=12)
plt.grid()
plt.show()

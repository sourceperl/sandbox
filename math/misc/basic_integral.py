from math import e
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np


def f_x(x: float) -> float:
    """sigmoid function"""
    return 1 / (1 + e**-x)


def approx_integral(func: Callable, start: float, stop: float, n_steps: int = 1_000) -> float:
    """
    Approximate the integral of a function using the trapezoidal rule.

    Parameters:
        func (Callable): The function to integrate. It should be a callable that takes a single float argument.
        start (float): The starting point of the integration interval.
        stop (float): The ending point of the integration interval.
        n_steps (int, optional): The number of steps to use in the approximation. Default is 1_000.

    Returns:
        The approximate value of the integral (float).
    """
    dx = (stop-start)/n_steps
    integral = 0.5 * (func(start) + func(stop)) * dx

    for i in range(1, n_steps):
        x_i = start + i * dx
        integral += func(x_i) * dx

    return integral


x_a, x_b = -2, 2
y_a, y_b = f_x(x_a), f_x(x_b)
y_max = max(y_a, y_b)
y_min = min(y_a, y_b)
integral = approx_integral(f_x, start=x_a, stop=x_b)
print(f'result = {integral}')

x = np.linspace(-5, 5, 1000)
y = np.vectorize(f_x)(x)

plt.plot(x, y)
plt.text(x_a + (x_b-x_a)/2, (y_max+y_min)/6, f'{integral:.02f}', horizontalalignment='center', fontsize=9)
plt.fill_between(x, y, where=(x >= x_a) & (x <= x_b), color='skyblue', alpha=0.4)
plt.axvline(x_a, color='orange', ls='--')
plt.axvline(x_b, color='orange', ls='--')
plt.grid()
plt.show()

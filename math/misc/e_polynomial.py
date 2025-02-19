from math import e, factorial

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial

# create a polynomial form equivalent to e**x (y = 1 + x + 1/2 x**2 + 1/24 x**3 + ...)
p_coefs = [1/factorial(n) for n in range(10)]
pol = Polynomial(p_coefs)

# e**x vs polynomial
x = np.linspace(0, 5, 1000)
y_e = e**x
y_pol = pol(x)

# plot
plt.plot(x, y_e, label='$e^x$')
plt.plot(x, y_pol, label='polynomial')
plt.legend()
plt.grid()
plt.show()

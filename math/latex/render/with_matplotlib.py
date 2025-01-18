import matplotlib.pyplot as plt
import numpy as np

# sigmoid in [-10, 10]
x = np.linspace(start=-10, stop=10, num=1_000)
y = 1 / (1 + np.exp(-x))

# plot it
plt.plot(x, y, c='orange')
plt.title('Sigmoid')
plt.xlabel(r'$x$')
plt.ylabel(r'$\sigma(x)$')
plt.text(2, 0.18, r'$\sigma(x)=\frac{1}{1+e^{-x}}$', fontsize=16, bbox=dict(boxstyle='round',
                                                                            ec=(0.0, 0.0, 0.0), fc=(1., 1, 1)))
plt.grid()
plt.show()

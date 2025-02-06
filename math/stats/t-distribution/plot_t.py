import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, t

x = np.arange(-4, 4, 0.01)


plt.plot(x, norm.pdf(x), linestyle='dashed', color='red', label='normal distribution')
plt.plot(x, t.pdf(x, df=1), label='T-distribution')
plt.legend()
plt.grid()
plt.show()

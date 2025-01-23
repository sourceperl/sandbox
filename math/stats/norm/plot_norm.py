import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

mean = 178.4
std_dev = 7.59
x = np.arange(140, 220, 0.01)


plt.plot(x, norm.pdf(x, mean, std_dev))
plt.plot(186, norm.pdf(186, mean, std_dev), color='red', marker='o')
plt.grid()
plt.show()

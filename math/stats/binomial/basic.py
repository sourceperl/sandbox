import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom

# 10 trials with a 50% probability of success
n = 10
p = 0.5

x = np.arange(1, n+1)
y = binom.pmf(k=x, n=n, p=p)

plt.bar(x=x, height=y)
plt.xlabel('number of successes')
plt.ylabel('probability of occurrence')
plt.grid()
plt.show()

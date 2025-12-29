import matplotlib.pyplot as plt
import numpy as np

# random dataset
np.random.seed(42)
a = np.random.rand(100)
b = np.random.rand(100)
sort_a = np.unique(a)

covariance = np.cov(a, b)[0, 1]
correlation = np.corrcoef(a, b)[0, 1]
linear_reg_poly = np.poly1d(np.polyfit(a, b, deg=1))
linear_reg_str = str(linear_reg_poly).strip()

print('random dataset:')
print(f'covariance  : {covariance:.3f}')
print(f'correlation : {correlation:.3f}')
print(f'regression  : {linear_reg_str}')

plt.subplot(211)
plt.title(f'random dataset (cov: {covariance:.3f}, cor: {correlation:.3f})')
plt.xlabel('a')
plt.ylabel('b')
plt.scatter(a, b, color='blue')
plt.plot(sort_a, linear_reg_poly(sort_a), color='red')
plt.grid(True, linestyle='--', alpha=0.7)

# linear dataset
a = np.random.rand(100)
b = 2*a + 5
sort_a = np.unique(a)

covariance = np.cov(a, b)[0, 1]
correlation = np.corrcoef(a, b)[0, 1]
linear_reg_poly = np.poly1d(np.polyfit(a, b, deg=1))
linear_reg_str = str(linear_reg_poly).strip()

print('\nlinear dataset:')
print(f'covariance  : {covariance:.3f}')
print(f'correlation : {correlation:.3f}')
print(f'regression  : {linear_reg_str}')

plt.subplot(212)
plt.title(f'linear dataset (cov: {covariance:.3f}, cor: {correlation:.3f})')
plt.xlabel('a')
plt.ylabel('b')
plt.scatter(a, b, color='blue')
plt.plot(sort_a, linear_reg_poly(sort_a), color='red')
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

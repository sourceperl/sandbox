"""
Régression linéaire par moindres carrés.

Génère un jeu de données bruité (y = 10x + 2 + bruit gaussien),
calcule manuellement la covariance et la variance pour en déduire
la pente et l'ordonnée à l'origine de la droite de régression
(méthode des moindres carrés), puis affiche le résultat.
"""

import matplotlib.pyplot as plt
import numpy as np

# samples
x = np.linspace(0, 100, 1000)
y = 10*x + 2
# add gaussian noise (mean: 0, standard deviation: 5)
y += np.random.normal(0, 5, size=x.shape)

# least squares method
n = len(x)
x_mean = x.mean()
y_mean = y.mean()

covariance = np.sum((x - x_mean) * (y - y_mean)) / n
variance = np.sum((x - x_mean)**2) / n

a = covariance / variance
b = y_mean - a * x_mean

# show
plt.scatter(x, y, color='red', marker='.', alpha=0.4, s=10, label='samples')
eq_sign = '-' if b < 0 else '+'
plt.plot(x, a*x + b, color='blue', linewidth=1, linestyle='--', label=f'y = {a:.2f}x {eq_sign} {abs(b):.2f}')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Régression linéaire par moindres carrés')
plt.legend()
plt.grid()
plt.show()

"""
Régression polynomiale par moindres carrés, degré paramétrable.

Génère un jeu de données bruité à partir d'un polynôme de référence,
calcule les coefficients via les équations normales et une matrice
de Vandermonde (méthode des moindres carrés : coeffs = (XᵀX)⁻¹Xᵀy),
puis affiche le résultat pour le degré choisi.
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

# params
DEGREE = 3
NOISE_STD = 5
REAL_COEFFS = [1, 2, -5, 3]


def format_equation(coeffs: NDArray, var_name: str = 'x', precision: int = 2) -> str:
    """
    Construit une chaîne lisible représentant un polynôme à partir de ses
    coefficients (ordre décroissant), avec les puissances en exposants
    Unicode (x², x³, ...).

    Exemple : format_equation([1, 2, -5, 3]) -> "y = x³ + 2.00x² - 5.00x + 3.00"
    """
    superscripts = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
    degree = len(coeffs) - 1

    terms = []
    for i, c in enumerate(coeffs):
        power = degree - i
        magnitude = abs(c)
        sign = '-' if c < 0 else '+'

        if power == 0:
            var_part = ''
        elif power == 1:
            var_part = var_name
        else:
            var_part = f'{var_name}{str(power).translate(superscripts)}'

        term = f'{magnitude:.{precision}f}{var_part}'

        if i == 0:
            terms.append(f'-{term}' if sign == '-' else term)
        else:
            terms.append(f'{sign} {term}')

    return 'y = ' + ' '.join(terms)


def rmse(y_true: NDArray, y_pred: NDArray) -> np.float64:
    """Root Mean Square Error entre valeurs observées et prédites."""
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


# samples
x = np.linspace(-10, 10, 1_000)
y = np.polyval(REAL_COEFFS, x)
# add gaussian noise (mean: 0, standard deviation: noise_std)
y += np.random.normal(0, NOISE_STD, size=x.shape)

# least squares method (parametrized degree polynomial)
# design matrix = Vandermonde matrix [x^degree, ..., x, 1]
X = np.vander(x, N=DEGREE + 1)

# normal equations: coeffs = (X^T X)^-1 X^T y
XtX = X.T @ X
Xty = X.T @ y
coeffs = np.linalg.solve(XtX, Xty)

y_fit = np.polyval(coeffs, x)
equation_str = format_equation(coeffs)
rmse_error = rmse(y, y_fit)

# show
plt.scatter(x, y, color='red', marker='.', alpha=0.4, s=10, label='samples')
plt.plot(x, y_fit, color='blue', linewidth=2, linestyle='--', label=equation_str)
plt.text(0.02, 0.95, f'RMSE = {rmse_error:.2f}', transform=plt.gca().transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Régression polynomiale (ordre {DEGREE}) par moindres carrés')
plt.legend()
plt.grid()
plt.show()

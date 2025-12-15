"""
This module provides a vectorized implementation of the Maclaurin (Taylor) series 
approximation for the sine function, sin(x). It pre-calculates the necessary 
inverse factorials for efficiency and allows the user to specify the order (number of terms) 
of the approximation for analysis.

The Maclaurin series for sin(x) is:
sin(x) = sum_{k=0}^{N} [ (-1)^k * x^(2k+1) / (2k+1)! ]
"""

from math import factorial

import matplotlib.pyplot as plt
import numpy as np

# optimization step: pre-calculate denominators (2*k + 1)!
# required factorials are 1!, 3!, 5!, 7!, ...
MAX_TERMS = 8
DENOM_K = np.array([factorial(2 * k + 1) for k in range(MAX_TERMS + 1)], dtype=np.float64)


def sin_approx(x: np.ndarray, num_terms: int) -> np.ndarray:
    """
    Computes the Maclaurin series approximation for sin(x) using pre-calculated denominators.

    This function is vectorized to operate efficiently on entire NumPy arrays.

    Args:
        x (np.ndarray): The input values in radians where the function is evaluated.
        num_terms (int): The number of terms (k=0 to num_terms-1) to use in the approximation.
                         E.g., num_terms=3 uses the terms for k=0, 1 and 2.

    Returns:
        np.ndarray: The approximated values of sin(x).
    """
    assert 0 < num_terms <= MAX_TERMS, f'The number of terms must be between 1 and {MAX_TERMS} (inclusive).'
    approx_sum = np.zeros_like(x)
    for k in range(num_terms):
        sign = (-1.0) ** k
        num = x ** (2 * k + 1)
        denom = DENOM_K[k]
        approx_sum += sign * num / denom
    return approx_sum


x = np.linspace(-4 * np.pi, 4 * np.pi, 1000)

plt.figure(figsize=(10, 6))
plt.title('Taylor series approximation of sin(x) near x=0')
plt.plot(x,  np.sin(x), label='np.sin(x)', color='blue', linewidth=2)
for n in range(1, 8, 2):
    y_approx = sin_approx(x, num_terms=n)
    plt.plot(x, y_approx, label=f'approx {n} term(s)', linestyle='--', alpha=0.8)
plt.xlabel('x (radians)')
plt.ylabel('y')
plt.grid()
plt.legend()
plt.xlim(-10, 10)
plt.ylim(-4, 4)
plt.show()
plt.show()

from sympy import pretty
from sympy.abc import x
from sympy.plotting import plot

# defines a polynomial
f = x**3 - 2*x**2 + 5*x - 1

# plot it
plot(f, (x, -5, +5), title=pretty(f, use_unicode=True))

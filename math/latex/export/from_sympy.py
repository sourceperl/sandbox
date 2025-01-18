import sympy as sp
from sympy.abc import x

# symbolic expression
y = sp.Integral(sp.sqrt(x**2 + 1), (x, 0, 1))

# to latex
print(sp.latex(y))

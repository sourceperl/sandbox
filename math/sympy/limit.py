from sympy import limit, oo, pretty
from sympy.abc import n

# define u(n)
u = (2 - n**2) / ((n + 1)*(n + 2))

# show u(n)
print('u(n):')
print(pretty(u) + '\n')

# find limit of u(n) for n -> +oo
print(f'limit of u(n) for n -> +oo: {limit(u, n, +oo)}')

import sympy as sp

# render latex formula at a 600 DPI png
latex_code = r'error = 100\times\frac{C_{ECV} - C_{AGA8}}{C_{AGA8}}'
sp.preview(f'$${latex_code}$$', dvioptions=['-D','600'])

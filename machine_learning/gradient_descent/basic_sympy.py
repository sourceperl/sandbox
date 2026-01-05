import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy.abc import x

# sympy setup
f_sp = (x - 5)**2
df_sp = sp.diff(f_sp, x)
print(df_sp)

# convert sympy expressions to fast numpy functions (allow vectorized inputs)
f_np = sp.lambdify(x, f_sp, 'numpy')
df_np = sp.lambdify(x, df_sp, 'numpy')

# parameters
x_init = 0.0
learning_rate = 0.1
iterations = 2_000
precision_target = 1e-9

x_value = x_init
x_history = [x_value]
y_history = [f_np(x_value)]

# optimization loop
for i in range(iterations):
    gradient = df_np(x_value)
    new_x = x_value - learning_rate * gradient

    # track progress
    x_history.append(new_x)
    y_history.append(f_np(new_x))

    # convergence check
    if abs(new_x - x_value) < precision_target:
        conv_msg = f'converged after {i} iterations'
        break
    x_value = new_x
else:
    conv_msg = 'reached maximum iterations'

# results string for the plot
results_text = (
    f'min at x: {x_value:.3f}\n'
    f'min f(x): {f_np(x_value):.3f}\n'
    f'{conv_msg}'
)

# improved visualization
fig, ax1 = plt.subplots(figsize=(10, 6))

# plot: the function and the descent path
# using f_num for the range generation
x_range = np.linspace(min(x_history)-4.0, max(x_history)+4.0, 2000)
ax1.plot(x_range, f_np(x_range), color='gray', alpha=0.3, label='f(x)')
ax1.scatter(x_history, y_history, c=range(len(x_history)), cmap='viridis', s=15, label='Descent path')
ax1.plot(x_value, f_np(x_value), 'ro', label='Final minimum')

# integrate results into the plot
ax1.text(0.05, 0.95, results_text, transform=ax1.transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

ax1.set_title(f'Gradient Descent Evolution (f(x) = ${sp.latex(f_sp)}$)')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.legend(loc='upper right')
ax1.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()

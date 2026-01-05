"""
gradient descent optimization script
this script implements a basic gradient descent algorithm to find the minimum
of a quadratic function f(x) = (x - 5)^2 and visualizes the path taken
"""

import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return (x - 5)**2


def dx_f(x):
    return 2*x - 10


# parameters
x = 0.0
learning_rate = 0.1
iterations = 2_000
precision_target = 1e-9

x_history = [x]
y_history = [f(x)]

# optimization loop
for i in range(iterations):
    gradient = dx_f(x)
    new_x = x - learning_rate * gradient

    # track progress
    x_history.append(new_x)
    y_history.append(f(new_x))

    # convergence check
    if abs(new_x - x) < precision_target:
        conv_msg = f'converged after {i} iterations'
        break
    x = new_x
else:
    conv_msg = 'reached maximum iterations'

# results string for the plot
results_text = (
    f'min at x: {x:.3f}\n'
    f'min f(x): {f(x):.3f}\n'
    f'{conv_msg}'
)

# improved visualization
fig, ax1 = plt.subplots(figsize=(10, 6))

# plot: the function and the descent path
x_range = np.linspace(min(x_history)-4.0, max(x_history)+4.0, 500)
ax1.plot(x_range, f(x_range), color='gray', alpha=0.3, label='f(x)')
ax1.scatter(x_history, y_history, c=range(len(x_history)), cmap='viridis', s=15, label='Descent path')
ax1.plot(x, f(x), 'ro', label='Final minimum')

# integrate print statement into the plot
# transform=ax1.transAxes uses relative coordinates (0 to 1) instead of data values
ax1.text(0.05, 0.95, results_text, transform=ax1.transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

ax1.set_title('Gradient Descent Evolution (f(x) = (x - 5)²)')
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.legend(loc='upper right')
ax1.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()

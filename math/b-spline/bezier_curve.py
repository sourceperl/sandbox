from math import comb

import matplotlib.pyplot as plt
import numpy as np

# some const
CTRL_POINTS = np.array([(1, 1), (3, 3), (5, 0), (7,3)])


# some functions
def bezier_at(t: float, ctrl_points: np.ndarray) -> np.ndarray:
    """Calculates a point on the Bézier curve at time t (t in [0; 1])."""

    # define polynomial degree and set start point (at (0,0))
    degree = len(ctrl_points) - 1
    bezier_pt = np.zeros(ctrl_points.shape[1])

    # B(t) = Σ P_k * B_{n,k}(t) for k from 0 to n
    for n in range(len(ctrl_points)):
        bernstein_weight = comb(degree, n) * t**(degree-n) * ((1 - t)**n)
        bezier_pt += ctrl_points[n] * bernstein_weight

    return bezier_pt


# generate the curve points (use 100 values of t between 0 and 1 for a smooth curve)
curve_points = np.array([bezier_at(t=t, ctrl_points=CTRL_POINTS) for t in np.linspace(0.0, 1.0, 100)])

# separate X and Y coordinates for plotting
ctrl_x = CTRL_POINTS[:, 0]
ctrl_y = CTRL_POINTS[:, 1]
curve_x = curve_points[:, 0]
curve_y = curve_points[:, 1]

# plotting
plt.figure(figsize=(10, 6))
# control polygon and points
plt.plot(ctrl_x, ctrl_y, linestyle='--', color='gray', alpha=0.6, label='Control Polygon')
plt.scatter(ctrl_x, ctrl_y, color='red', s=80, zorder=5, label='Control Points')
# add control point labels
for i in range(len(CTRL_POINTS)):
    txt = chr(ord('A') + i)
    plt.annotate(txt, (ctrl_x[i] + 0.1, ctrl_y[i] - 0.1), fontsize=12, weight='bold')
# Bézier Curve
plt.plot(curve_x, curve_y, color='blue', linewidth=3, label='Bézier Curve')

# plot
plt.title(f'Bézier Curve')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
plt.axis('equal')
plt.show()

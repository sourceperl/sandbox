"""
Lorenz system

https://en.wikipedia.org/wiki/Lorenz_system
"""

import matplotlib.pyplot as plt


def lorenz_sim(n: int, dt: float = 0.01, sigma: float = 10.0, rho: float = 28.0, beta: float = 8/3) -> tuple:
    # initial position is (1, 1, 1)
    x, y, z = (1.0, 1.0, 1.0)
    x_l, y_l, z_l = [x], [y], [z]

    # compute the next position after a time step dt
    for _ in range(n-1):
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x += dx
        y += dy
        z += dz
        x_l.append(x)
        y_l.append(y)
        z_l.append(z)

    return x_l, y_l, z_l


# simulate system for 3000 steps
x_l, y_l, z_l = lorenz_sim(n=3_000)

# 3d plot
ax = plt.axes(projection='3d')
ax.plot(x_l, y_l, z_l, color='orange')
ax.set_title('Lorenz system')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()

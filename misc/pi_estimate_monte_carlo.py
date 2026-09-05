import numpy as np

# nombre de tirages
n = 10_000_000

# génération de n points (x, y) uniformément distribués sur [0, 1[
x = np.random.random(n)
y = np.random.random(n)

# calcul des distances à l'origine
distances = np.sqrt(x**2 + y**2)

# comptage des points situés dans le quart de cercle (distance <= 1)
in_circle = distances <= 1.0
n_inside_circle = np.sum(in_circle)

# estimation de pi
pi_estimate = 4.0 * n_inside_circle / n

print(f'estimation de pi (Monte-Carlo) : {pi_estimate:.6f}')
print(f'erreur : {pi_estimate - np.pi:.6f}')

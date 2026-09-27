"""
Générateur de fractale de Mandelbrot en haute résolution.

Utilise numpy pour le calcul vectorisé et matplotlib pour le rendu.
Le coloriage utilise l'algorithme du "smooth coloring" (échappement lissé)
pour éviter les bandes de couleur nettes.

https://fr.wikipedia.org/wiki/Ensemble_de_Mandelbrot
https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.colors import LinearSegmentedColormap

# ============================== CONFIGURATION ==============================

WIDTH, HEIGHT = 3840, 2160        # Résolution de l'image (ici : 4K)
MAX_ITER = 500                    # Nombre max d'itérations (détail / netteté)

# Zone du plan complexe à afficher (par défaut : vue d'ensemble classique)
# Attention au rapport largeur (réels) /hauteur (imaginaires): idéalement ratio de 16/9)
REAL_MIN, REAL_MAX = -2.2, 0.8
IM_MIN, IM_MAX = -1.3, 1.3

# Pour zoomer sur une zone intéressante, décommentez et ajustez par exemple :
# REAL_MIN, REAL_MAX = -0.748, -0.744
# IM_MIN, IM_MAX = 0.078, 0.082
# MAX_ITER = 1000

OUTPUT_FILE = "outputs/mandelbrot.png"
DPI = 300                         # Résolution d'export (points par pouce)

# =============================================================================


def build_mandelbrot(width: int, height: int, real_min: float, real_max: float, im_min: float, im_max: float,
                     max_iter: int) -> npt.NDArray[np.float64]:
    """
    Calcule la fractale de Mandelbrot de façon vectorisée avec numpy.

    Retourne un tableau 2D de valeurs "lissées" représentant la vitesse
    d'échappement de chaque point (utilisé ensuite pour la coloration).
    """

    # Grille de nombres complexes correspondant à chaque pixel (x: réels, y: imaginaires)
    reals = np.linspace(real_min, real_max, width, dtype=np.float64)
    ims = np.linspace(im_min, im_max, height, dtype=np.float64)
    C = reals[np.newaxis, :] + 1j * ims[:, np.newaxis]

    Z = np.zeros_like(C, dtype=np.complex128)
    # Compteur d'itérations avant échappement (initialisé à max_iter = "n'échappe pas")
    iterations = np.full(C.shape, max_iter, dtype=np.float64)
    mask = np.ones(C.shape, dtype=bool)  # points encore "actifs" (pas encore échappés)

    # Pour le "smooth coloring" on conserve |Z| au moment de la sortie
    Z_abs_at_escape = np.zeros(C.shape, dtype=np.float64)

    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + C[mask]

        escaped = np.abs(Z) > 2.0
        newly_escaped = escaped & mask

        iterations[newly_escaped] = i
        Z_abs_at_escape[newly_escaped] = np.abs(Z[newly_escaped])

        mask &= ~escaped
        if not mask.any():
            break

    # Smooth coloring : on ajoute une correction continue pour éviter les
    # bandes de couleur nettes entre deux niveaux d'itération entiers.
    with np.errstate(divide="ignore", invalid="ignore"):
        # + d'infos: https://linas.org/art-gallery/escape/escape.html
        smooth = iterations + 1 - np.log(np.log(np.clip(Z_abs_at_escape, 1e-10, None))) / np.log(2)

    # Les points qui n'échappent jamais (toujours à l'intérieur de l'ensemble) restent à max_iter
    smooth[iterations >= max_iter] = max_iter

    return smooth


def build_colormap() -> LinearSegmentedColormap:
    """Palette de couleurs personnalisée, du bleu profond à l'orange/blanc."""
    colors = [
        (0.0, "#000764"),
        (0.16, "#206bcb"),
        (0.42, "#edffff"),
        (0.6425, "#ffaa00"),
        (0.8575, "#000200"),
        (1.0, "#000000"),
    ]
    positions = [c[0] for c in colors]
    hexcolors = [c[1] for c in colors]
    return LinearSegmentedColormap.from_list("mandelbrot", list(zip(positions, hexcolors)))


if __name__ == "__main__":
    # retrouve le chemin de sortie pour la production de l'image finale (relatif au script lui même)
    base_dir = Path(__file__).resolve().parent
    img_path = base_dir / OUTPUT_FILE

    print(f"Calcul de la fractale ({WIDTH}x{HEIGHT}, {MAX_ITER} itérations max)...")
    mandel_matrix = build_mandelbrot(WIDTH, HEIGHT, REAL_MIN, REAL_MAX, IM_MIN, IM_MAX, MAX_ITER)

    print("Rendu de l'image...")

    fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI)

    # occupe toute la figure, sans marges
    ax = fig.add_axes((0, 0, 1, 1))
    ax.axis("off")

    cmap = build_colormap()
    ax.imshow(mandel_matrix, cmap=cmap, extent=(REAL_MIN, REAL_MAX, IM_MIN, IM_MAX),
              origin="lower", interpolation="bilinear",)

    # exporte l'image
    print(f"Enregistre l'image sous : {img_path}")
    fig.savefig(img_path, dpi=DPI, facecolor="black")
    plt.close(fig)

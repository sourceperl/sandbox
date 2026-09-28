"""
Render a LaTeX math formula to a PNG image using Matplotlib's mathtext.
"""


from pathlib import Path

import matplotlib.pyplot as plt


def latex_to_png(
    formula: str,
    output_path: str | Path,
    font_size: int = 20,
    dpi: int = 300,
    color: str = "black",
    transparent: bool = False,
    padding: float = 0.1,
) -> Path:
    """Render a LaTeX math formula to a PNG image using Matplotlib's mathtext.

    Args:
        formula: LaTeX math expression, without the surrounding ``$`` delimiters.
        output_path: Destination path of the PNG file. Missing parent
            directories are created automatically.
        font_size: Font size of the rendered formula, in points.
        dpi: Resolution of the output image.
        color: Text color (any Matplotlib color specification).
        transparent: If True, the background is transparent instead of white.
        padding: Padding around the formula, in inches.

    Returns:
        The path of the generated PNG file.

    Raises:
        ValueError: If the formula cannot be parsed by mathtext.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure()
    try:
        fig.text(0, 0, f"${formula}$", fontsize=font_size, color=color)
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight", pad_inches=padding, transparent=transparent)
    except ValueError as exc:
        raise ValueError(f"Invalid LaTeX formula: {formula!r}") from exc
    finally:
        plt.close(fig)

    return output_path


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    img_path = base_dir / "outputs" / "latex.png"

    f = r"\zeta(s) = \sum_{n=1}^{\infty}\frac{1}{n^s}" \
        r" = \prod_{p\ \mathrm{prime}}\frac{1}{1 - p^{-s}}"

    latex_to_png(formula=f, output_path=img_path)
    print(f"Image saved to {img_path}")

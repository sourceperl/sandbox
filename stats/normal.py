""" Plot a normal distribution. """

import math
import matplotlib.pyplot as plt


# some functions
def my_range(start: float, stop: float, step: float, ndig_round: int = 10):
    while start <= stop:
        yield start
        start = round(start + step, ndig_round)


def normal_pdf(x: float, mean: float, std_dev: float) -> float:
    """
    Compute the probability density function (PDF) of the normal distribution.

    Parameters:
    - x: The value for which to calculate the PDF.
    - mean: The mean of the normal distribution (also called mu).
    - std_dev: The standard deviation of the normal distribution (also called sigma).

    Returns:
    The PDF value at the given x.
    """
    coefficient = 1 / (std_dev * math.sqrt(2 * math.pi))
    exponent = -((x - mean)**2) / (2 * std_dev**2)
    return coefficient * math.exp(exponent)


if __name__ == '__main__':
    # draw pdf plot for [-5.0, +5.0] with mu=0.0 and sigma=1.0
    mean, std_dev = 0.0, 1.0
    x, y = [], []
    for x_value in my_range(start=-5.0, stop=5.0, step=0.01):
        x.append(x_value)
        y.append(normal_pdf(x_value, mean, std_dev))

    plt.plot(x, y)
    plt.grid()
    plt.show()

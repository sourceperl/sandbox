""""
Ulam Spiral

https://en.wikipedia.org/wiki/Ulam_spiral
"""

import math

import matplotlib.pyplot as plt
import numpy as np


# some functions
def is_prime(n) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


# some class
class Grid:
    def __init__(self, width: int, height: int) -> None:
        # public
        self.width = width
        self.height = height
        # private
        self._grid = np.zeros((self.width, self.height))

    @property
    def as_array(self) -> np.ndarray:
        return self._grid

    @property
    def bounding_box(self) -> tuple:
        return -self.width/2, self.width/2, self.height/2, -self.height/2

    def set_pixel(self, x: int, y: int, value: float):
        self._grid[y + self.height // 2][x + self.width // 2] = value


class SpiralIterator:
    def __init__(self, width: int, height: int, clockwise: bool = True):
        # public
        self.width = width
        self.height = height
        self.clockwise = clockwise
        # private
        self._x = 0
        self._y = 0
        self._dir_x = 1
        self._dir_y = 0
        self._steps = 0

    @property
    def total_steps(self):
        return self.width * self.height

    def __iter__(self):
        return self

    def __next__(self):
        if self._steps >= self.total_steps:
            raise StopIteration
        self._steps += 1

        # on corner
        if self.clockwise:
            corner_up_right = self._x > 0 and self._x == 1 - self._y
            corner_other = abs(self._x) == abs(self._y) and (self._dir_x, self._dir_y) != (1, 0)
            if corner_up_right or corner_other:
                # update direction of travel (→ to ↓, ↓ to ←, ← to ↑, ↑ to →)
                self._dir_x, self._dir_y = -self._dir_y, self._dir_x
        else:
            corner_down_right = self._x > 0 and self._x == 1 + self._y
            corner_other = abs(self._x) == abs(self._y) and (self._dir_x, self._dir_y) != (1, 0)
            if corner_down_right or corner_other:
                # update direction of travel (→ to ↑, ↑ to ←, ← to ↓, ↓ to →)
                self._dir_x, self._dir_y = self._dir_y, -self._dir_x

        # move to next position
        current_position = (self._x, self._y)
        self._x += self._dir_x
        self._y += self._dir_y
        return current_position


if __name__ == '__main__':
    # init prime grid (use an odd number for width and height)
    grid = Grid(width=151, height=151)

    # draw spiral
    n = 1
    for x, y in SpiralIterator(width=grid.width, height=grid.height, clockwise=False):
        grid.set_pixel(x, y, 0 if is_prime(n) else 1)
        n += 1

    # show prime grid
    plt.imshow(grid.as_array, extent=grid.bounding_box, cmap='gray', vmin=0, vmax=1)
    plt.title('Ulam spiral', size=20)
    plt.show()

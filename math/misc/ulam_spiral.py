""""
Ulam Spiral

https://en.wikipedia.org/wiki/Ulam_spiral

!!! WORK IN PROGRESS !!!
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
        self.width = width if width % 2 else width+1
        self.height = height if height % 2 else height+1
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
    def __init__(self, width: int, height: int):
        # public
        self.width = width
        self.height = height
        # private
        self._x = 0
        self._y = 0
        self._dx = 1
        self._dy = 0
        self._steps = 0

    @property
    def total_steps(self):
        return self.width * self.height

    def __iter__(self):
        return self

    def __next__(self):
        if self._steps >= self.total_steps:
            raise StopIteration

        # on corner
        if abs(self._x) == abs(self._y) and (self._dx, self._dy) != (1, 0) or self._x > 0 and self._y == 1 - self._x:
            # change direction
            self._dx, self._dy = -self._dy, self._dx

        # if abs(self._x) > self.width / 2 or abs(self._y) > self.height / 2:
        #     # change direction
        #     self._dx, self._dy = -self._dy, self._dx
        #     # jump
        #     self._x, self._y = -self._y + self._dx, self._x + self._dy

        current_position = (self._x, self._y)
        self._x, self._y = self._x + self._dx, self._y + self._dy
        self._steps += 1

        return current_position


if __name__ == '__main__':
    # init prime grid
    grid = Grid(width=15, height=15)

    # draw spiral
    i = 0
    for x, y in SpiralIterator(width=grid.width, height=grid.height):
        #print(x, y)
        grid.set_pixel(x, y, i)
        i += 1

    # show prime grid
    plt.imshow(grid.as_array, extent=grid.bounding_box)
    plt.title('Ulam spiral', size=20)
    plt.show()

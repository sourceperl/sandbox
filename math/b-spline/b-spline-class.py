import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splprep


class MyBSpline:
    def __init__(self, tck: tuple) -> None:
        self.tck = tck

    @property
    def tck_x(self) -> tuple:
        t, (c_x, c_y), k = self.tck
        return (t, c_x, k)

    @property
    def tck_y(self) -> tuple:
        t, (c_x, c_y), k = self.tck
        return (t, c_y, k)

    def _B(self, u: float, k: int, i: int, t: list) -> float:
        """
        Manually computes the value of the i-th B-spline basis function B(u)
        of degree k (order k+1) defined by the knot vector t, at parameter u.

        This function uses the Cox-de Boor recursive formula.

        Args:
            u (float): The parameter value (on the curve domain) to evaluate at.
            k (int): The degree of the B-spline basis function.
            i (int): The index of the basis function.
            t (list): The non-decreasing list of knot values (knot vector).

        Returns:
            float: The value of the basis function B_i,k(u).
        """
        # Base case: Degree 0 B-spline (piecewise constant function)
        if k == 0:
            # B_i,0(u) is 1.0 if u is in the half-open interval [t_i, t_{i+1}), otherwise 0.0
            return 1.0 if t[i] <= u < t[i+1] else 0.0

        # First term coefficient calculation (c1)
        # Term is zero if the denominator (t_{i+k} - t_i) is zero (i.e., multiple knots)
        if t[i+k] == t[i]:
            c1 = 0.0
        else:
            # c1 = (u - t_i) / (t_{i+k} - t_i) * B_{i, k-1}(u)
            c1 = (u - t[i])/(t[i+k] - t[i]) * self._B(u, k-1, i, t)

        # Second term coefficient calculation (c2)
        # Term is zero if the denominator (t_{i+k+1} - t_{i+1}) is zero
        if t[i+k+1] == t[i+1]:
            c2 = 0.0
        else:
            # c2 = (t_{i+k+1} - u) / (t_{i+k+1} - t_{i+1}) * B_{i+1, k-1}(u)
            c2 = (t[i+k+1] - u)/(t[i+k+1] - t[i+1]) * self._B(u, k-1, i+1, t)

        # The B-spline of degree k is the sum of the two lower-degree terms
        return c1 + c2

    def _bspline(self, u: float, t: list, c: list, k: int) -> float:
        """
        Computes a point on the B-spline curve by summing the basis functions
        multiplied by their corresponding control points (coefficients).

        S(u) = sum(c_i * B_i,k(u)) for all relevant i.

        Args:
            u (float): The parameter value to evaluate at.
            t (list): The knot vector.
            c (list): The B-spline coefficients (control points).
            k (int): The degree of the spline.

        Returns:
            float: The evaluated spline value S(u).
        """
        # The number of basis functions (and non-zero control points) is n.
        # Relationship: len(t) = n + k + 1. Thus, n = len(t) - k - 1.
        n = len(t) - k - 1

        # Assertions for B-spline consistency (n must be >= k+1, and len(c) must be >= n)
        assert (n >= k+1) and (len(c) >= n), "Inconsistent t, c, and k parameters for B-spline."

        # Summation S(u) = sum_{i=0}^{n-1} c_i * B_{i,k}(u).
        # Since B_{i,k}(u) has local support, most terms will be 0.0, calculated by the B() function.
        return sum(c[i] * self._B(u, k, i, t) for i in range(n))

    def get_pos(self, u: float) -> tuple:
        x = self._bspline(u, *self.tck_x)
        y = self._bspline(u, *self.tck_y)
        return (x, y)


# main path definition
coords = [(10, 10), (30, 45), (60, 40), (30, 60), (10, 10)]
coords_x, coords_y = zip(*coords)
plt.plot(coords_x, coords_y, 'bo', label='Original points')

# Calculate the B-spline representation (tck) for a 2D curve
# splprep is used for parametric curve fitting ([x(u), y(u)]).
# s=0 (interpolation): Force the spline to pass exactly through the points.
# k=3 (cubic): Cubic spline degree.
# per=1 (periodic/closed): Creates a closed loop, ensuring C^(k-1) continuity at start/end points.
tck, _u_range = splprep([coords_x, coords_y], s=0, k=3, per=1)

my_b_spline = MyBSpline(tck)
x_l, y_l = [], []

# Loop through parameter values (u)
# np.linspace(0.0, 1.0, 10) samples 10 points between u=0 (start) and u=1 (end) of the fitted curve.
for u in np.linspace(0.0, 1.0, 100):
    # Print comparison: SciPy's optimized BSpline object vs. the manual bspline() function
    x, y = my_b_spline.get_pos(u)
    x_l.append(x)
    y_l.append(y)

plt.plot(x_l, y_l, color='orange', linewidth=2)

plt.grid()
plt.legend(loc='best')
plt.show()

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splprep


class BSpline:
    def __init__(self, tck: tuple) -> None:
        # a tuple containing the vector (knots, B-spline coefficients, degree of the spline)
        self.tck = tck

    def __call__(self, u: float) -> float:
        """
        Computes a point on the B-spline curve by summing the basis functions
        multiplied by their corresponding control points (coefficients).

        S(u) = sum(c_i * B_i,k(u)) for all relevant i.

        Args:
            u (float): The parameter value to evaluate at.
            tck (tuple): The (t, c, k) tuple for the specific coordinate (X or Y).

        Returns:
            float: The evaluated spline value S(u).
        """
        # extract
        t, c, k = self.tck

        # number of basis functions (and non-zero control points) is n.
        # relationship: len(t) = n + k + 1. Thus, n = len(t) - k - 1.
        n = len(t) - k - 1

        # assertions for B-spline consistency (n must be >= k+1, and len(c) must be >= n)
        if (n < k+1) or (len(c) < n):
            raise ValueError('inconsistent tck parameters for B-spline.')

        # summation S(u) = sum_{i=0}^{n-1} c_i * B_{i,k}(u).
        # since B_{i,k}(u) has local support, most terms will be 0.0, calculated by the B() function.
        return sum(c[i] * self._b(u, k, i, t) for i in range(n))

    @staticmethod
    def _b(u: float, k: int, i: int, t: list) -> float:
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
        # base case: Degree 0 B-spline (piecewise constant function)
        if k == 0:
            # B_i,0(u) is 1.0 if u is in the half-open interval [t_i, t_{i+1}), otherwise 0.0
            return 1.0 if t[i] <= u < t[i+1] else 0.0

        # first term coefficient calculation (c1)
        # term is zero if the denominator (t_{i+k} - t_i) is zero (i.e., multiple knots)
        if t[i+k] == t[i]:
            c1 = 0.0
        else:
            c1 = (u - t[i])/(t[i+k] - t[i]) * BSpline._b(u, k-1, i, t)

        # second term coefficient calculation (c2)
        # term is zero if the denominator (t_{i+k+1} - t_{i+1}) is zero
        if t[i+k+1] == t[i+1]:
            c2 = 0.0
        else:
            c2 = (t[i+k+1] - u)/(t[i+k+1] - t[i+1]) * BSpline._b(u, k-1, i+1, t)

        # the B-spline of degree k is the sum of the two lower-degree terms
        return c1 + c2


# main path definition
ref_pts = [(10, 10), (30, 45), (60, 40), (30, 60), (10, 10)]
ref_pts_x, ref_pts_y = zip(*ref_pts)


# Calculate the B-spline representation (tck) for a 2D curve
# splprep is used for parametric curve fitting ([x(u), y(u)]).
# s=0 (interpolation): Force the spline to pass exactly through the points.
# k=3 (cubic): Cubic spline degree.
# per=1 (periodic/closed): Creates a closed loop, ensuring C^(k-1) continuity at start/end points.
tck, _u_range = splprep([ref_pts_x, ref_pts_y], s=0, k=3, per=1)
t, (c_x, c_y), k = tck

# build 100 points for path [(x0, y0 for u0), (x1, y1 for u1), ...]
path_pts = []
for u in np.linspace(0.0, 1.0, 100):
    path_pts.append((BSpline(tck=(t, c_x, k))(u), BSpline(tck=(t, c_y, k))(u)))
path_x, path_y = zip(*path_pts)

# show data with matplotlib
plt.title('B-Spline path')
plt.plot(ref_pts_x, ref_pts_y, color='blue', marker='o', linestyle='None', label='original points')
plt.plot(path_x, path_y, color='orange', linestyle='--', linewidth=2, label='b-spline path')
plt.grid()
plt.legend(loc='best')
plt.show()

import numpy as np


class ThomasAlgorithm:
    def __init__(self, a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def solve(self):
        n = len(self.d)
        b, c, d = self.b.copy(), self.c.copy(), self.d.copy()

        # Forward stroke.
        for i in range(1, n):
            b[i] = b[i] - self.a[i-1] * c[i-1] / b[i-1]
            d[i] = d[i] - self.a[i-1] * d[i-1] / b[i-1]

        # Reverse stroke.
        y = np.zeros(n+1)
        y[n-1] = d[n-1] / b[n-1]
        for i in range(n-2, -1, -1):
            y[i] = (d[i] - c[i] * y[i+1]) / b[i]

        return y

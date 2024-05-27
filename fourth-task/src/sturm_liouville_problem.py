from math import sqrt, cos, sin
import numpy as np

from thomas import ThomasAlgorithm


class SturmLiouvilleProblem:

    def __init__(self, n, h, lam, xs, ys):
        self.n = n
        self.h = h
        self.lam = lam
        self.xs = xs
        self.ys = ys

    def get_lambda_sqrt(self):
        return sqrt(self.lam)

    def define_ys(self):

        alg = ThomasAlgorithm(a=np.zeros(self.n),
                              b=np.zeros(self.n),
                              c=np.zeros(self.n),
                              d=np.zeros(self.n))

        for i in range(1, self.n + 1):
            j = i - 1

            if i >= 1:
                alg.a[j] = self.get_system_left_side(i - 1, i)
            if i < self.n:
                alg.c[j] = self.get_system_left_side(i + 1, i)
            alg.b[j] = self.get_system_left_side(j, j)
            alg.d[j] = self.get_system_right_side(j)

        result = alg.solve()  # Use Thomas algorithm.
        result[0], result[self.n] = 0, 0
        self.ys = result

    def get_system_left_side(self, j, k):
        # This function uses immediately calculated integrals.
        j, k = min(j, k), max(j, k)

        if k - j == 0:
            return (self.xs[j + 1] + self.lam * self.xs[j] ** 2 * self.xs[j + 1] - self.lam *
                    self.xs[j] * self.xs[j + 1] ** 2 + (self.lam* self.xs[j + 1] ** 3) /
                    3 - self.xs[j - 1] - self.lam * self.xs[j] ** 2 * self.xs[j - 1] +
                    self.lam * self.xs[j] * self.xs[j - 1] ** 2 - (self.lam * self.xs[j - 1] ** 3) / 3) / (self.h ** 2)
        if k - j == 1:
            return (-1 / 6.0) * (-6 + self.lam * (self.xs[j] - self.xs[j - 1]) ** 2) * (self.xs[j] - self.xs[j + 1]) / (self.h ** 2)
        return 0

    def get_system_right_side(self, j):
        # This function uses immediately calculated integrals.
        return float(2 * (- self.get_lambda_sqrt() * (self.xs[j] - self.xs[j + 1]) * cos(self.get_lambda_sqrt() * self.xs[j]) + sin(self.get_lambda_sqrt() * self.xs[j]) - sin(self.get_lambda_sqrt() * self.xs[j + 1])) + 2 * (- self.get_lambda_sqrt() * (self.xs[j] - self.xs[j - 1]) * cos(self.get_lambda_sqrt() * self.xs[j]) + sin(self.get_lambda_sqrt() * self.xs[j]) - sin(self.get_lambda_sqrt() * self.xs[j - 1]))) / self.h

    def get_basic_function(self, x, j):

        if j == self.n:
            if self.xs[self.n - 1] <= x and x <= self.xs[self.n]:
                return (x - self.xs[self.n - 1]) / self.h

        if j == 0:
            if 0 <= x and x <= self.xs[1]:
                return (self.xs[1] - x) / self.h

        if self.xs[j - 1] <= x and x <= self.xs[j]:
            return (x - self.xs[j-1]) / self.h

        if self.xs[j] <= x and x <= self.xs[j+1]:
            return (self.xs[j+1] - x) / self.h

        return 0

    def get_approximate_value(self, x):
        left_border = 0
        right_border = self.n

        while right_border - left_border > 1:
            middle = (right_border + left_border) // 2
            if x > self.xs[middle]:
                left_border = middle
            else:
                right_border = middle

        left_basic_function = self.get_basic_function(x, left_border)
        right_basic_function = self.get_basic_function(x, right_border)

        return self.ys[left_border] * left_basic_function + self.ys[right_border] * right_basic_function


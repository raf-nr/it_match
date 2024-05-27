import numpy as np

from sturm_liouville_problem import SturmLiouvilleProblem
from scipy.integrate import quad


class Errors:
    @staticmethod
    def get_f(x, lam):
        return -2 * lam * np.sin(np.sqrt(lam) * x)

    @staticmethod
    def get_norm(lam, left_b, right_b):
        sq_fun = lambda x: (Errors.get_f(x, lam)) ** 2
        res, _ = quad(sq_fun, left_b, right_b)
        return np.sqrt(res)

    @staticmethod
    def get_error(sl_problem: SturmLiouvilleProblem, right_b):
        j_m = 0.15
        c = sl_problem.lam * right_b ** 2 / 4 + 1
        c_prime = j_m * np.sqrt(c)

        real_values = np.array([np.sin(np.sqrt(sl_problem.lam) * (i*sl_problem.h)) for i in range(sl_problem.n)])
        approx_values = np.array([sl_problem.get_approximate_value(i * sl_problem.h) for i in range(sl_problem.n)])

        right = (c * c_prime)**2 * sl_problem.h**2 * Errors.get_norm(sl_problem.lam, 0, right_b)
        left = np.sqrt(np.sum((real_values - approx_values)**2) * sl_problem.h)
        if left > right:
            print(f"The theoretical assessment was NOT confirmed. Error {left} is bigger than {right}")
        else:
            print(f"The theoretical assessment was confirmed. Error: {left}")

        return left
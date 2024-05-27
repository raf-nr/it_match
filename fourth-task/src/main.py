from math import pi
import numpy as np

from errors import Errors
from sturm_liouville_problem import SturmLiouvilleProblem

if __name__ == '__main__':

    b_list = [(0, 1*pi), (0, 2*pi), (0, 3*pi)]
    n_list = [10, 20, 30, 40, 50]

    print("\n <---------- RESULTS ----------> \n")
    for b in b_list:
        for n in n_list:
                print(f"BORDER = {b}, N = {n} \n")
                left_border, right_border = b
                h = (right_border - left_border) / n
                xs = np.linspace(left_border, right_border, n+1)

                problem = SturmLiouvilleProblem(n, h, (pi/right_border)**2, xs, np.zeros(1))
                problem.define_ys()
                Errors.get_error(problem, right_border)
                print("\n <-----------------------------> \n")


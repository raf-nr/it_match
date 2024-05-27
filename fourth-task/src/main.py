
from sturm_liouville_problem import SturmLiouvilleProblem

if __name__ == '__main__':

    b_list = []
    l_list = []
    n_list = []

    print("\n <---------- RESULTS ----------> \n")
    for b in b_list:
        for n in n_list:
            for l in l_list:
                print(f"BORDER = {b}, N = {n}, LAMBDA={l} \n")
                left_border, right_border = b
                h = (right_border - left_border) / n
                xs = np.linspace(left_border, right_border, n+1)

                problem = SturmLiouvilleProblem(n, h, l, xs, np.zeros(1))
                problem.define_ys()
                # Error.get_error(problem, right_border)
                print("\n <-----------------------------> \n")
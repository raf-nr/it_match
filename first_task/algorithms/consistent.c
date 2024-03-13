#include <math.h>
#include <stdio.h>
#include "omp.h"
#include "common.c"

uint32_t consistent(appnet_t *net, double eps) {
    uint32_t iter = 0;
    int32_t n = net->n;
    double h = net->h;
    double** u = net->u;
    double** f = net->f;
    double dmax;

    do {
        dmax = 0; // Maximum change in u values
        iter++;
        for (int i = 1; i < n + 1; i++) {
            for (int j = 1; j < n + 1; j++) {
                double temp = u[i][j];
                u[i][j] = 0.25 * (u[i - 1][j] + u[i + 1][j] + u[i][j - 1] + u[i][j + 1] - h * h * f[i][j]);
                double dm = fabs(temp - u[i][j]);
                dmax = fmax(dmax, dm);
            }
        }
    } while (dmax > eps);
    return iter;
}

void run_consistent(int32_t n, int32_t threads, func f, func g, double eps) {
    uint32_t iter = 0;
    appnet_t *net = create_appnet(n, f, g);

    omp_set_num_threads(threads);
    double start_time = omp_get_wtime();
    iter = consistent(net, eps);
    double end_time = omp_get_wtime();
    double time_difference = end_time - start_time;
    printf("Time: %0.3f, Iterations amount: %d \n", time_difference, iter);
}
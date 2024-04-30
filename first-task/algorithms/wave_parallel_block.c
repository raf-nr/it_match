#include <math.h>
#include <stdint.h>
#include <stdio.h>
//#include "omp.h"
#include "consistent.c"

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) > (b)) ? (a) : (b))

double approximate_block(appnet_t *my_net, int i, int j, uint32_t block_size) {
    int iStart = 1 + i * block_size;
    int iEnd = MIN(iStart + block_size - 1, my_net->n);
    int jStart = 1 + j * block_size;
    int jEnd = MIN(jStart + block_size - 1, my_net->n);

    double dmax = 0;
    for (int i= iStart; i<= iEnd; i++) {
        for (int j= jStart; j<= jEnd; j++) {
            double temp = my_net->u[i][j];
            my_net->u[i][j] = 0.25 * (my_net->u[i- 1][j] + my_net->u[i][j- 1] + my_net->u[i+ 1][j] +
                                      my_net->u[i][j+ 1] - my_net->h * my_net->h * my_net->f[i][j]);
            double dm = fabs(temp - my_net->u[i][j]);
            dmax = MAX(dmax, dm);
        }
    }

    return dmax;
}

uint32_t approximate(appnet_t *my_net, double eps, uint32_t block_size) {
    uint32_t iter = 0;
    int num_block = my_net->n / block_size + (my_net->n % block_size != 0);
    double *dm = calloc(num_block, sizeof(*dm));
    int i, j;
    double d, dmax;

    do {
        iter++;
        dmax = 0;
        for (int nx = 0; nx < num_block; nx++) {
            dm[nx] = 0;

#pragma omp parallel for shared(nx, dm) private(i, j, d)
            for (i = 0; i <= nx; i++) {
                j = nx - i;
                d = approximate_block(my_net, i, j, block_size);
                dm[i] = MAX(d, dm[i]);
            }
        }

        for (int nx = num_block - 1; nx >= 1; nx--) {
#pragma omp parallel for shared(nx, dm) private(i, j, d)
            for (i = num_block - nx; i < num_block; i++) {
                j = 2 * (num_block - 1) - nx - i + 1;
                d = approximate_block(my_net, i, j, block_size);
                dm[i] = MIN(d, dm[i]);
            }
        }

        for (int i = 0; i < num_block; i++) {
            dmax = MAX(dmax, dm[i]);
        }

    } while (dmax > eps);
    free(dm);
    return iter;
}

void run_parallel_block(int32_t n, int32_t threads, func f, func g, double eps, uint32_t block_size) {
    uint32_t iter = 0;
    appnet_t *net = create_appnet(n, f, g);

    omp_set_num_threads(threads);
    double start_time = omp_get_wtime();
    iter = approximate(net, eps, block_size);
    double end_time = omp_get_wtime();
    double time_difference = end_time - start_time;
    printf("Time: %0.8f, Iterations amount: %d \n", time_difference, iter);
}

#include <math.h>
#include <stdio.h>
#include "omp.h"
#include "common.c"

uint32_t alg(appnet_t *net, double eps) {
    int32_t n = net->n;
    double h = net->h;
    double** u = net->u;
    double** f = net->f;
    double dmax;

    uint32_t iter = 0;

    // Граничные значения u задаются при постановке задачи
    // Граничные значения не изменяются внутри циклов
    do {
        dmax = 0; // Максимальное изменение значений u
        iter++;
        // Обходим все внутренние узлы сетки
        for (int i = 1; i < n + 1; i++) {
            for (int j = 1; j < n + 1; j++) {
                double temp = u[i][j];
                // Уточняем значение u[i][j] по формуле
                u[i][j] = 0.25 * (u[i - 1][j] + u[i + 1][j] + u[i][j - 1] + u[i][j + 1] - h * h * f[i][j]);
                double dm = fabs(temp - u[i][j]);
                // Обновляем максимальное изменение
                dmax = fmax(dmax, dm);
            }
        }
    } while (dmax > eps); // Повторяем до тех пор, пока максимальное изменение больше заданной точности eps
    return iter;
}

void run(int32_t n, int32_t threads, int32_t repeats, func f, func g, double eps) {
    double avr = 0;

    appnet_t *net = create_appnet(n, f, g);

    omp_set_num_threads(threads);

    uint32_t iter = 0;

    for (int i = 0; i < repeats; ++i) {
        double start_time = omp_get_wtime();
        iter = alg(net, eps);
        double end_time = omp_get_wtime();
        double time_difference = end_time - start_time;
        avr += time_difference;
    }
    printf("Time: %f, Iterations amount: %d \n", avr / repeats, iter);
}
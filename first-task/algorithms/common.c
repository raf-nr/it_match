#include <stdlib.h>

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) > (b)) ? (a) : (b))

typedef double (*func)(double, double);

typedef int32_t n_array[];
typedef int threads_array[];

typedef struct _appnet_ {
    int32_t n;
    double h;

    double** u;
    double** f;
} appnet_t;

void free_matrix(double **arr, int32_t n) {
    if (arr == NULL)
        return;

    for (int i = 0; i < n; i++) {
        free(arr[i]);
    }
    free(arr);
}

double **allocate_matrix(int32_t n) {
    double **arr = (double **)malloc(n * sizeof(double *));
    if (arr == NULL)
        return NULL;

    for (int i = 0; i < n; i++) {
        arr[i] = (double *)calloc(n, sizeof(double));
        if (arr[i] == NULL) {
            free_matrix(arr, i);
            return NULL;
        }
    }
    return arr;
}

double randfrom(double min, double max) {
    double range = (max - min);
    double div = RAND_MAX / range;
    return min + (rand() / div);
}

appnet_t *create_appnet(int32_t n, func f, func g) {
    appnet_t *my_net = malloc(sizeof(*my_net));
    if (my_net == NULL)
        return NULL;

    my_net->n= n;
    my_net->h = 1.0 / (n + 1);
    my_net->u = allocate_matrix(n + 2);
    my_net->f = allocate_matrix(n + 2);

    if (my_net->u == NULL || my_net->f == NULL) {
        // If an error occurs, free the already allocated memory and return NULL.
        free_matrix(my_net->u, n + 2);
        free_matrix(my_net->f, n + 2);
        free(my_net);
        return NULL;
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            my_net->f[i][j] = f(i * my_net->h, j * my_net->h);
        }
    }

    for (int i = 0; i <= n + 1; i++) {
        for (int j = 0; j <= n + 2; j++) {

            if ((i == 0) || (j == 0) || (i == (n + 1)) || (j == (n + 1))) {
                my_net->u[i][j] = g(i * my_net->h, j * my_net->h);
            } else {
                my_net->u[i][j] = 0;
            }

        }
    }

    return my_net;
}

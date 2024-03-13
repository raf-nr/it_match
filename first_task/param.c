#include <math.h>

#define BLOCK_SIZE 64
#define EPS 0.1
#define N_ARRAY {100}
#define THREADS_ARRAY {1, 2, 4, 8, 12, 16}

double d_kx3_p_2ky3(double x, double y) { return 6000 * x + 12000 * y; }

double kx3_p_2ky3(double x, double y) { return 1000 * pow(x, 3) + 2000 * pow(y, 3); }
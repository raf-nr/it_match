#include <math.h>

#define BLOCK_SIZE 64
#define EPS 0.1
#define N_ARRAY {50, 100, 200, 300, 400, 500, 1000, 2000, 3000, 4000}
#define THREADS_ARRAY {1, 2, 4, 8, 10}

double f_declr (double x, double y) { return 6000 * x + 12000 * y; }

double g_declr (double x, double y) { return 1000 * pow(x, 3) + 2000 * pow(y, 3); }
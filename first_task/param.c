#include <math.h>

#define BLOCK_SIZE 64
#define EPS 0.01
#define N_ARRAY {50, 100, 200, 300, 400, 500, 750, 1000, 2000, 3000}
#define THREADS_ARRAY {8}

double f_declr1 (double x, double y) { return 900 * pow(x, 8) + 900 * pow(y, 8); }
double g_declr1 (double x, double y) { return 10 * pow(x, 10) + 10 * pow(y, 10); }

double f_declr2 (double x, double y) { return 0; }
double g_declr2 (double x, double y) { return 100 * (1 - 2 * x) * (1 - 2 * y); }

double f_declr3 (double x, double y) { return -100 * y * sin(x) - 100 * x * sin(y); }
double g_declr3 (double x, double y) { return 100 * x * sin(y) + 100 * y * sin(x); }

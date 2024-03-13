#include <stdio.h>
#include <stdint.h>

#include "param.c"
#include "algorithms/wave_parallel_block.c"

int main(){
    static const n_array n = N_ARRAY;
    int32_t n_amount = sizeof(n) / sizeof(n[0]);

    static const threads_array threads = THREADS_ARRAY;
    uint32_t threads_amount = sizeof(threads) / sizeof(threads[0]);

    func f = f_declr;
    func g = g_declr;

    for (int i = 0; i < n_amount; ++i) {
        for (int j = 0; j < threads_amount; ++j) {
            printf("\n--------------------------------------- \n");
            printf("N: %d, Threads: %d \n \n", n[i], threads[j]);
            printf("CONSISTENT ALGORITHM: ");
            run_consistent(n[i], threads[j], f, g, EPS);
            printf("PARALLEL ALGORITHM: ");
            run_parallel_block(n[i], threads[j], f, g, EPS, BLOCK_SIZE);
            printf("--------------------------------------- \n \n \n");
        }
    }
    return 0;
}
#include <stdio.h>
#include <stdint.h>

#include "param.c"
#include "consistent.c"
#include "wave_parallel_block.c"

int main(){
    // Определение массивов размеров и числа потоков
    static const n_array n = N_ARRAY;
    int32_t n_amount = sizeof(n) / sizeof(n[0]);

    static const threads_array threads = THREADS_ARRAY;
    uint32_t threads_amount = sizeof(threads) / sizeof(threads[0]);

    for (int i = 0; i < n_amount; ++i) {
        for (int j = 0; j < threads_amount; ++j) {
            printf("\n--------------------------------------- \n");
            printf("N: %d, Threads: %d \n \n", n[i], threads[j]);
            printf("CONSISTENT ALGORITHM: ");
            run(n[i], threads[j], 1, d_kx3_p_2ky3, kx3_p_2ky3, EPS);
            printf("PARALLEL ALGORITHM: ");
            run_p(n[i], threads[j], 1, d_kx3_p_2ky3, kx3_p_2ky3, EPS, BLOCK_SIZE);
            printf("--------------------------------------- \n \n \n");
        }
    }
    return 0;
}
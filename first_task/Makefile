CC = gcc

.PHONY: clean all

all: main2

main1: main.c Makefile
	gcc main.c -fopenmp -lm -o main

main2: main.c Makefile
	gcc main.c -fopenmp -lm -O3 main

clean:
	rm -rf main
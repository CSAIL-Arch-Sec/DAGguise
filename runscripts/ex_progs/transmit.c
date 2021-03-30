#include <stdio.h>
#include <stdlib.h>

#define NUM_ACCESS 2000
#define DEPENDENT


int main (void) {
	register volatile int dump1 = 0;
	register volatile int dump2 = 0;
	register volatile int dump3 = 0;

	register int *probe = calloc(64, 16384); //Probe array

	// Create a random array which indexes itself
	for(int i = 0; i < 512; i++) {
		probe[i * 256] = rand() % 512;
	}

	printf("NOW\n");

	// Perform either independent or dependent load instructions (trying to avoid hitting the cache)
	register int i = 0;
	while(++i){
		#ifdef DEPENDENT
		dump1 = probe[256 * dump3];
		dump2 = probe[256 * dump1];
		dump3 = probe[256 * dump2];
		#endif
		#ifndef DEPENDENT
		dump1 = probe[256 * (i % 512)];
		dump2 = probe[256 * ((i+16) % 512)];
		dump3 = probe[256 * ((i+32) % 512)];
		#endif
	}
	
	return 0;
}

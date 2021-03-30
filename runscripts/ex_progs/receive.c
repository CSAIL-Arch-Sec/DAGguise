#include <stdio.h>
#include <stdlib.h>
#include <gem5/m5ops.h>

#define NUM_ACCESS 1000

int main (void) {
	register volatile int dump = 0;

	register int *probe = malloc(64*65536); //Probe array

	//asm(".rept 10000000; nop; .endr");

	//m5_reset_stats(0,0);
	//m5_dump_stats(0,0);

	m5_start_defence();

	for(register int i = 0; i < NUM_ACCESS; i++) {
		dump = probe[256 * i];
	}

	m5_end_defence();
	//m5_dump_stats(0,0);

	printf("DONE \n");
	return 0;
}

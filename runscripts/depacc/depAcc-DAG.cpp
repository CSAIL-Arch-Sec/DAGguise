#include "zsim_hooks.h"

#define MEMSIZE (1024*1024)
#define ROWSIZE (1024*4)  //row size is 1024*4 Byte

//#define NUM_MEMACCESS 8 * 16  // unroll to 8
#define NUM_MEMACCESS 8 * 1  // unroll to 8


int main()
{
  zsim_roi_begin();
  // Init the aligned array
  int* array_unaligned = new int[(MEMSIZE + ROWSIZE) / sizeof(int)];
  int* array = (int*)((unsigned long)((array_unaligned+ROWSIZE/sizeof(int))) & (unsigned long)~(ROWSIZE/sizeof(int)-1));
  volatile int a;
  volatile int depA[NUM_MEMACCESS+1]; depA[0] = 0; int zero = 0;
  int rowOffset = 0;

  zsim_heartbeat();  // This start to get DAG
  // Real start
  for (int memAccessID = 0; memAccessID < NUM_MEMACCESS; memAccessID += 8) {
    depA[memAccessID + 1] = (array[depA[memAccessID + 0]] & zero) + 1*ROWSIZE / sizeof(int) + rowOffset;
    depA[memAccessID + 2] = (array[depA[memAccessID + 1]] & zero) + 2*ROWSIZE / sizeof(int) + rowOffset;
    depA[memAccessID + 3] = (array[depA[memAccessID + 2]] & zero) + 3*ROWSIZE / sizeof(int) + rowOffset;
    depA[memAccessID + 4] = (array[depA[memAccessID + 3]] & zero) + 4*ROWSIZE / sizeof(int) + rowOffset;

    depA[memAccessID + 5] = (array[depA[memAccessID + 4]] & zero) + 5*ROWSIZE / sizeof(int) + rowOffset;
    depA[memAccessID + 6] = (array[depA[memAccessID + 5]] & zero) + 6*ROWSIZE / sizeof(int) + rowOffset;
    depA[memAccessID + 7] = (array[depA[memAccessID + 6]] & zero) + 7*ROWSIZE / sizeof(int) + rowOffset;
    depA[memAccessID + 8] = (array[depA[memAccessID + 7]] & zero) + 8*ROWSIZE / sizeof(int) + rowOffset;

    rowOffset += 8*ROWSIZE / sizeof(int);
  }
  zsim_heartbeat();  // This end to get DAG
  zsim_roi_end();
  
  return 0;
}
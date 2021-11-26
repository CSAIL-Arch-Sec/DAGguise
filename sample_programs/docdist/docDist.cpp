#include<iostream>
#include<fstream>
#include<map>
#include<string>
#include<math.h>
#include "zsim_hooks.h"
using namespace std;

#define REF_START 0
#define REF_NUM 230

#define USER_START 237
#define USER_NUM 1

#define DATASET_DIR string("/data/scratch/pwd/zsim-src/scripts/docDist-DAG/dataset/properSizeTxt/")

//#define USE_ZSIM_FAST_FORWARD
//#define SKIP_10K_MEMACC
#define DUMP_CHECKPOINT 
//#define GET_SHORT_DAG
 
 
typedef std::map<std::string,int> strintmap;
 
 
void countwords(std::istream &in, strintmap &words){
    std::string s;
    while (in >> s){
        ++words[s];
    }
}
 
int computedistance(strintmap& d1, strintmap& d2){
    int dotproduct = 0;
    int i = 0;
    for (strintmap::iterator p1 = d1.begin(); p1 != d1.end(); p1++){
        printf("Iteration %d\n", i++);
        strintmap::iterator p2 = d2.find(p1->first);
        if (p2 != d2.end())
            dotproduct += (p1->second*p2->second);
    }
    return dotproduct;
}
 
int main(int argc, char* argv[]){

    // STEP1: read the files
    ifstream refFile[REF_NUM], userFile[USER_NUM];
    for (int i = 0; i < REF_NUM; i++) {
        refFile[i].open(DATASET_DIR + to_string(REF_START+i) + string(".txt"), ios::in);
    }
    for (int i = 0; i < USER_NUM; i++) {
        userFile[i].open(DATASET_DIR + to_string(USER_START+i) + string(".txt"), ios::in);
    }


    // STEP2: change file into map
    strintmap refDoc[REF_NUM], userDoc[USER_NUM];
    for (int i = 0; i < REF_NUM; i++) {
        countwords(refFile[i], refDoc[i]);
    }
    for (int i = 0; i < USER_NUM; i++) {
        countwords(userFile[i], userDoc[i]);
    }

#ifdef DUMP_CHECKPOINT
  __asm__ __volatile__ (".word 0x040F; .word 0x0043;" : : "D" (0), "S" (0) :);
#endif

    zsim_roi_begin();
#ifndef GET_SHORT_DAG
    zsim_heartbeat();  // This start to get DAG
#endif

    // STEP3: compare file
    int dotproduct[USER_NUM][REF_NUM];
    for (int i = 0; i < USER_NUM; i++) {
        for (int j = 0; j < REF_NUM; j++) {
            printf("User num: %d, Ref num: %d\n", i, j);
#ifdef GET_SHORT_DAG
            if (j==50) { zsim_heartbeat(); }
            if (j==55) { zsim_heartbeat(); zsim_roi_end(); }
#endif
            dotproduct[i][j] = computedistance(userDoc[i], refDoc[j]);
        }
    }

#ifndef GET_SHORT_DAG
    zsim_heartbeat(); zsim_roi_end(); // This end to get DAG
#endif
    

    cout << "--finish--" << "\n";
    return 0;
}

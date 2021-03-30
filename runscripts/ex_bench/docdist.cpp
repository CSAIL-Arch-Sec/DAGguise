#include<iostream>
#include<fstream>
#include<map>
#include<string>
#include<math.h>
 
#define pi   3.14159265358979323846264338327950288419716939937510
 
using namespace std;
 
typedef std::map<std::string,int> strintmap;
 
 
void countwords(std::istream &in, strintmap &words){
    std::string s;
 
    while (in >> s){
        ++words[s];
    }
}
 
int modit(strintmap d){
    int mod=0;
    for (strintmap::iterator p = d.begin(); p != d.end(); p++){
        mod += p->second * p->second;
    }
    return mod;
}
 
int computedistance(strintmap d1, strintmap d2){
    int dotproduct = 0;
    for (strintmap::iterator p1 = d1.begin(); p1 != d1.end(); p1++){
        for (strintmap::iterator p2 = d2.begin(); p2 != d2.end(); p2++){
            if (p1->first == p2->first)
                dotproduct += (p1->second*p2->second);
        }
    }
    return dotproduct;
}
 
int main(){
 
    std::ifstream f1,f2;
    int dotproduct;
    int mod1, mod2;
    double mod;
    float distance;         //distance between the documents
     
 
    //initialize the file pointers
    f1.open("file1.txt", ios::in);
    f2.open("file2.txt", ios::in);
     
    if (!f1)
        std::cout << "file 1 error ";
    if (!f2)
        std::cout << "file 2 error";
 
    strintmap d1,d2;
 
    countwords(f1, d1);
    countwords(f2, d2);
 
    /*for (strintmap::iterator p = d1.begin(); p != d1.end() ; p++){
        std::cout << p->first << "  occured " << p->second << " times " << std::endl;
    }
     
    std::cout << std::endl;
 
    for (strintmap::iterator p = d2.begin(); p != d2.end(); p++){
        std::cout << p->first << "  occured " << p->second << " times " << std::endl;
    }*/
     
    dotproduct = computedistance(d1, d2);
    //std::cout << std::endl << " the distance is " << dotproduct<<std::endl;
    mod1 = modit(d1);
    mod2 = modit(d2);
    mod = sqrt(mod1*mod2);
 
 
    distance = 180*acos(dotproduct / mod)/pi;
     
    //std::cout << std::endl << "the value is  " << value << std::endl;
 
    std::cout << "the distance between the docments is " << distance << "\n";
 
    return 0;
}

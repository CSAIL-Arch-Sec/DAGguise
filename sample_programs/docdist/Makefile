all: docDist
docDist_checkpoint: docDist.cpp zsim_hooks.h
	g++ -static docDist.cpp -o docDist_checkpoint -DDUMPCHECKPOINT 
docDist: docDist.cpp zsim_hooks.h
	g++ -static docDist.cpp -o docDist 


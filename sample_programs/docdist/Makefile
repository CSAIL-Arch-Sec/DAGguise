all: docDist docDist_checkpoint
docDist_checkpoint: docDist.cpp zsim_hooks.h
	g++ -static docDist.cpp -o docDist_checkpoint -DDUMP_CHECKPOINT 
docDist: docDist.cpp zsim_hooks.h
	g++ -static docDist.cpp -o docDist 


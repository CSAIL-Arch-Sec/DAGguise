all: transmit receive
transmit: transmit.c
	gcc -static -I../../include/ -I../../util/m5 ../../util/m5/m5op_x86.S transmit.c -o transmit

receive: receive.c
	gcc -static -I../../include/ -I../../util/m5 ../../util/m5/m5op_x86.S receive.c -o receive 




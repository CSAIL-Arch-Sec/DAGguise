./build/X86/gem5.opt \
	./configs/example/se.py \
	--cpu-type=DerivO3CPU \
	--num-cpus=1 \
	--mem-type=DRAMSim2 \
	--caches --l1d_size=32kB --l1i_size=32kB \
        --l1d_assoc=8 --l1i_assoc=8 \
	--l2cache --l3cache \
	--l2_size=512kB --l2_assoc=16 \
	--l3_size=2MB --l3_assoc=16 \
        --cpu-clock=2.4GHz --sys-clock=2.4GHz \
	--mem-size=4GB \
	-c 'runscripts/docdist/docDist-DAG' \
        -o 'runscripts/docdist/1word-1.txt runscripts/docdist/diff100000.txt'

	#--debug-flags=Cache \

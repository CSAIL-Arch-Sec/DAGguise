./build/X86/gem5.opt \
	--debug-flags=PseudoInst \
	./configs/example/se.py \
	--cpu-type=DerivO3CPU \
	--num-cpus=2 \
	--mem-type=DRAMSim2 \
	--caches --l1d_size=256B --l1i_size=1kB \
	--mem-size=4GB \
	-c 'runscripts/ex_bench/docdist;runscripts/ex_progs/receive'


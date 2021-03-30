./build/X86/gem5.opt \
	--debug-flags=PseudoInst,Cache \
	./configs/example/se.py \
	--cpu-type=DerivO3CPU \
	--num-cpus=1 \
	--mem-type=DRAMSim2 \
	--caches --l1d_size=32MB --l1i_size=32MB \
        --l1d_assoc=8 --l1i_assoc=8 \
	--l2cache --l3cache \
	--l2_size=512MB --l2_assoc=16 \
	--l3_size=2MB --l3_assoc=16 \
	--mem-size=4GB \
	-c 'runscripts/depacc/depAcc-DAG'


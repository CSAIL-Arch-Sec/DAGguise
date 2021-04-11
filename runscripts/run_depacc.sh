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
	--mem-size=4GB --enabledramlog \
        --dramdeviceconfigfile=/home/peter/Desktop/gem5_19/gem5/ext/dramsim2/DRAMSim2/ini/DDR3_micron_32M_8B_x8_sg125.ini \
        --dramsystemconfigfile=/home/peter/Desktop/gem5_19/gem5/ext/dramsim2/DRAMSim2/system_fsbta.ini \
        --dagprotectionfile=/home/peter/Desktop/gem5_19/gem5/defence/def.json \
        --enabledramlog \
	-c 'runscripts/depacc/depAcc-DAG'


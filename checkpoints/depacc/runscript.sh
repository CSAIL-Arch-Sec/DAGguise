#!/bin/bash

export SIM_DESC=0

/home/pwd/gem5_checkpoint_19/build/X86/gem5.opt \
        --outdir=m5_mergetest \
	/home/pwd/gem5_checkpoint_19/configs/example/se.py \
	--cpu-type=AtomicSimpleCPU \
	--num-cpus=1 \
	--mem-type=DRAMSim2 \
	--caches --l1d_size=32kB --l1i_size=32kB \
        --l1d_assoc=8 --l1i_assoc=8 \
	--l2cache --l3cache \
	--l2_size=512kB --l2_assoc=16 \
	--l3_size=1MB --l3_assoc=16 \
        --cpu-clock=2.4GHz --sys-clock=2.4GHz \
	--mem-size=4GB --enabledramlog \
        --dramdeviceconfigfile=/home/pwd/gem5_checkpoint_19/ext/dramsim2/DRAMSim2/ini/DDR3_micron_32M_8B_x8_sg125.ini \
        --dramsystemconfigfile=/home/pwd/gem5_checkpoint_19/ext/dramsim2/DRAMSim2/system_reg.ini \
        --dagprotectionfile=/home/pwd/gem5_checkpoint_19/defence/docdist/defenseDAG_0W0N_10000avg.json \
	-c '/home/pwd/zsim-src/scripts/depAcc-DAG/build/depAcc-DAG' \
	--checkpoint-dir=/home/pwd/gem5_checkpoint_19/checkpoints/depacc/ \

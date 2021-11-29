#!/bin/bash

$GEM5_ROOT/build/X86/gem5.opt \
        --outdir=/data/scratch/pwd/artifact_eval/gem5_19/sensitivity/out_baseline \
	$GEM5_ROOT/configs/example/se.py \
	--cpu-type=DerivO3CPU \
	--num-cpus=1 \
	--mem-type=DRAMSim2 \
	--caches --l1d_size=32kB --l1i_size=32kB \
        --l1d_assoc=8 --l1i_assoc=8 \
	--l2cache --l3cache \
	--l2_size=256kB --l2_assoc=16 \
	--l3_size=1MB --l3_assoc=16 \
        --cpu-clock=2.4GHz --sys-clock=2.4GHz \
        --checkpoint-restore=1 --maxinsts=50000000 --warmup-insts=1000000 --standard-switch=1000000 \
        --checkpoint-dir=$GEM5_ROOT/checkpoint/docdist/ \
	--mem-size=4GB --enabledramlog \
        --dramdeviceconfigfile=$GEM5_ROOT/ext/dramsim2/DRAMSim2/ini/DDR3_micron_32M_8B_x8_sg125.ini \
        --dramsystemconfigfile=$GEM5_ROOT/ext/dramsim2/DRAMSim2/configs/system_reg_multi.ini \
	-c "$GEM5_ROOT/sample_programs/docdist/docDist" \
	--dagprotectionfile=/data/scratch/pwd/artifact_eval/gem5_19/sensitivity/0_1/0_1.json\
	--dramsim2outputfile=/data/scratch/pwd/artifact_eval/gem5_19/sensitivity/out_baseline/out_baseline \

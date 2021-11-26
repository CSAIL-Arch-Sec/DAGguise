#!/bin/sh

mkdir -p merge_ckpt/$1/$2
python $GEM5_ROOT/util/checkpoint_aggregator.py -o merge_ckpt/$1/$2 --memory-size=4294967296 --cpts $2 $3


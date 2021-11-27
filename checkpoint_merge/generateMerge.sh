#!/bin/sh

mkdir -p merge_ckpt
python $GEM5_ROOT/util/checkpoint_aggregator.py -o merge_ckpt --memory-size=4294967296 --cpts $2 $3


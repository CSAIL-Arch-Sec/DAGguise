#!/bin/sh

mkdir -p $1
python $GEM5_ROOT/util/checkpoint_aggregator.py -o $1 --memory-size=4294967296 --cpts $2 $3


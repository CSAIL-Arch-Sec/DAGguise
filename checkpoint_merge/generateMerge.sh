#!/bin/bash

pattern="^(.*\/){0,1}(.*\/.*\/.*)$"
[[ $2 =~ $pattern ]]

localdir="${BASH_REMATCH[2]}"
echo $localdir

mkdir -p $1/$localdir
python2 $GEM5_ROOT/util/checkpoint_aggregator.py -o $1/$localdir --memory-size=4294967296 --cpts $2 $3


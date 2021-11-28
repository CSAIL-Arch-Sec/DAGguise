if [[ -z "$GEM5_ROOT" ]]; then
    echo "GEM5_ROOT is not set!" 1>&2
    exit 1
fi

if [[ -z "$SPEC_ROOT" ]]; then
    echo "SPEC_ROOT is not set!" 1>&2
    exit 1
fi

# Change if desired
VICTIM_CHECKPOINT="$GEM5_ROOT/checkpoint/docdist/cpt.1285668325407/"

cd $GEM5_ROOT/checkpoint_merge/
export GEM5_ROOT
export VICTIM_CHECKPOINT
condor_submit merge_checkpoints.condor
cd -

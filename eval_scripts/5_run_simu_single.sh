if [[ -z "$GEM5_ROOT" ]]; then
    echo "GEM5_ROOT is not set!" 1>&2
    exit 1
fi

if [[ -z "$SPEC_ROOT" ]]; then
    echo "SPEC_ROOT is not set!" 1>&2
    exit 1
fi

# Change if desired
victim_checkpoint="$GEM5_ROOT/checkpoints/docdist/cpt.1379571884454/"
unprotected_checkpoint="$SPEC_ROOT/ckpt/bwaves_r/cpt.None.SIMP-0/"

cd $GEM5_ROOT/checkpoint_merge/
source generateMerge.sh merged_checkpoint $unprotected_checkpoint $victim_checkpoint
cd -

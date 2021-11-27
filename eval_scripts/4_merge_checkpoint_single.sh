if [[ -z "$GEM5_ROOT" ]]; then
    echo "GEM5_ROOT is not set!" 1>&2
    exit 1
fi

if [[ -z "$SPEC_ROOT" ]]; then
    echo "SPEC_ROOT is not set!" 1>&2
    exit 1
fi

# Change if desired
victim_checkpoint="$GEM5_ROOT/checkpoint/docdist/cpt.1285668325407/"
unprotected_checkpoint="$SPEC_ROOT/ckpt/bwaves_r/cpt.None.SIMP-0/"

cd $GEM5_ROOT/checkpoint_merge/
export GEM5_ROOT
bash generateMerge.sh merged_checkpoint/cpt.None.SIMP-0/ $unprotected_checkpoint $victim_checkpoint
cd -

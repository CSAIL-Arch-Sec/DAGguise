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

[ ! -d $victim_checkpoint ] && echo "Specified checkpoint doesn't exist! The checkpoint pointer in this script may need to be updated to point to the correct path/tick id." && exit 1

cd $GEM5_ROOT/checkpoint_merge/
export GEM5_ROOT
bash generateMerge_single.sh merged_checkpoint/cpt.None.SIMP-0/ $unprotected_checkpoint $victim_checkpoint
cd -

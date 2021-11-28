if [[ -z "$GEM5_ROOT" ]]; then
    echo "GEM5_ROOT is not set!" 1>&2
    exit 1
fi

if [[ -z "$SPEC_ROOT" ]]; then
    echo "SPEC_ROOT is not set!" 1>&2
    exit 1
fi

export TEST_NAME="docDist_2cpu_closedrow_private"

cd $GEM5_ROOT/eval_scripts/simu_condor/
python3 generateRunscripts.py $GEM5_ROOT/eval_scripts/simu_common/$TEST_NAME.sh

cd $SPEC_ROOT/
condor_submit $GEM5_ROOT/eval_scripts/simu_condor/launch.condor
cd -

if [[ -z "$GEM5_ROOT" ]]; then
    echo "GEM5_ROOT is not set!" 1>&2
    exit 1
fi

if [[ -z "$SPEC_ROOT" ]]; then
    echo "SPEC_ROOT is not set!" 1>&2
    exit 1
fi

cd $GEM5_ROOT/plot_scripts/
python3 plot_2cpu.py $GEM5_ROOT/eval_scripts/simu_condor/results/ docDist_2cpu_DAGguise docDist_2cpu_FSBTA docDist_2cpu_regular
cd -

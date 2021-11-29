if [[ -z "$GEM5_ROOT" ]]; then
    echo "GEM5_ROOT is not set!" 1>&2
    exit 1
fi

if [[ -z "$SPEC_ROOT" ]]; then
    echo "SPEC_ROOT is not set!" 1>&2
    exit 1
fi

# First, queue up the DAGguise execution 
export TEST_NAME="docDist_2cpu_DAGguise"

cd $GEM5_ROOT/sensitivity/
python3 generateRunscripts.py $GEM5_ROOT/sensitivity/template.sh

#cd $SPEC_ROOT/
#condor_submit $GEM5_ROOT/sensitivity/launch.condor
#cd -

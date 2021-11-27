if [[ -z "$GEM5_ROOT" ]]; then
    echo "GEM5_ROOT is not set!" 1>&2
    exit 1
fi

cd $GEM5_ROOT/sample_programs/docdist
make
cd $GEM5_ROOT/checkpoints/docdist
source runscript.sh
cd -

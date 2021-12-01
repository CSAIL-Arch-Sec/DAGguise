if [[ -z "$GEM5_ROOT" ]]; then
    echo "GEM5_ROOT is not set!" 1>&2
    exit 1
fi

cd $GEM5_ROOT
scons -j32 build/X86/gem5.opt
cd -

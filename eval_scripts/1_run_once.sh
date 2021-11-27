if [[ -z "$SPEC_ROOT" ]]; then
    echo "SPEC_ROOT is not set!" 1>&2
    exit 1
fi

# The pre-existing checkpoints are for a slightly older version of gem5, so let's patch them
sed -i -e 's/itb.walker\]/itb.walker\]\ncurrPwrState=0/g' -e 's/dtb.walker\]/dtb.walker\]\ncurrPwrState=0/g' -e 's/mem_ctrls\]/mem_ctrls\]\ncurrPwrState=0/g' -e 's/system.cpu.workload.ptable.Entry/system.cpu.workload.Entry/g' $SPEC_ROOT/ckpt/*/cpt.None.SIMP-*/m5.cpt

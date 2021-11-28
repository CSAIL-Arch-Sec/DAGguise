import os
import sys
import subprocess
from shutil import copyfile

gem5root = os.environ.get('GEM5_ROOT')
specroot = os.environ.get('SPEC_ROOT')

assert(gem5root is not None)
assert(specroot is not None)

rundir = "./run/"
ckptdir = gem5root + "/checkpoint_merge/merged_checkpoint/"
resultsdir = gem5root + "/eval_scripts/simu_simple/results/"
dramsim2File = resultsdir + "dram"


benchmark = 'bwaves_r'
chkptNum = 0
assert(len(sys.argv) > 1)

runscriptFile = 'runscript.sh'

copyfile(sys.argv[1], runscriptFile)
runHandle = open(runscriptFile, "a+")

runHandle.write('\t--checkpoint-dir=/%s/\\\n' % ckptdir)
runHandle.write('\t--benchmark='+benchmark+' \\\n')
runHandle.write('\t--simpt-ckpt='+str(chkptNum)+' \\\n')
runHandle.write('\t--dramsim2outputfile=%s \\\n' % (dramsim2File))

runHandle.close()

subprocess.call(["sed", "-i", "-e", 's|OUTDIR_REPLACE|%s|g' % resultsdir, runscriptFile])
subprocess.call(["chmod", "+777", runscriptFile])
    

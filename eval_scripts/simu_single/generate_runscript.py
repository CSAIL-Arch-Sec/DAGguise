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

benchmark = 'bwaves_r'
chkptNum = 0
assert(len(sys.argv) > 1)

destFile = 'runscript.sh'

copyfile(sys.argv[1], destFile)
runHandle = open(destFile, "a+")

runHandle.write('\t--checkpoint-dir=/%s/\\\n' % ckptdir)
runHandle.write('\t--benchmark='+benchmark+' \\\n')
runHandle.write('\t--simpt-ckpt='+str(chkptNum)+' \\\n')

runHandle.close()

os.makedirs(rundir, exist_ok=True)
os.makedirs(os.path.join(rundir, 'results', 'DDR3_micron_32M_8B_x8_sg125', '4GB.1Ch.8R.scheme2.close_page.32TQ.32CQ.RtB.pRankpBank'), exist_ok=True)
subprocess.call(["sed", "-i", "-e", 's/DRAM_REPLACE/dram/g', destFile])
subprocess.call(["sed", "-i", "-e", 's/OUTDIR_REPLACE/output/g', destFile])
subprocess.call(["chmod", "+777", destFile])
    

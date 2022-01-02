import os
import sys
import subprocess
from shutil import copyfile

gem5root = os.environ.get('GEM5_ROOT')
specroot = os.environ.get('SPEC_ROOT')

assert(gem5root is not None)
assert(specroot is not None)

rundir = specroot + "/run/"
ckptdir = gem5root + "/checkpoint_merge/merged_checkpoint/"
resultsdir = gem5root + "/eval_scripts/simu_condor/results/"

exprs = ['blender_r', 'bwaves_r', 'cactuBSSN_r', 'cam4_r', 'deepsjeng_r', 'exchange2_r', 'fotonik3d_r', 'lbm_r', 'leela_r', 'nab_r', 'mcf_r', 'namd_r', 'parest_r', 'povray_r','roms_r', 'wrf_r', 'x264_r', 'xz_r']
#exprs = ['bwaves_r']

assert(len(sys.argv) > 1)

os.makedirs(resultsdir, exist_ok=True)

for dirname in os.listdir(rundir):
    if(dirname[-1] != 'r' or (dirname not in exprs)): continue
    for ckptname in next(os.walk(os.path.join(ckptdir, dirname)))[1]:
        chkptNum = int(ckptname.split('-')[1])
        testname = sys.argv[1].split('/')[-1].split('.')[0]

        outdirpath=os.path.join(resultsdir, testname, dirname, str(chkptNum))
        os.makedirs(outdirpath,exist_ok=True)
        subprocess.call(["chmod", "-R", "+777", os.path.join(resultsdir, testname)])

        runscriptFile = os.path.join(resultsdir, testname, dirname, testname + '_' + str(chkptNum) + "_runscript.sh")
        dramsim2File = os.path.join(resultsdir, testname, dirname, testname + '_' + str(chkptNum) + "_dram.vis")
        outdir = os.path.join(resultsdir, testname, dirname, str(chkptNum)) 
        
        copyfile(sys.argv[1], runscriptFile)
        runHandle = open(runscriptFile, "a+")

        runHandle.write('\t--checkpoint-dir=/%s/%s/\\\n' % (ckptdir,dirname))
        runHandle.write('\t--dramsim2outputfile=%s \\\n' % (dramsim2File))
        runHandle.write('\t--benchmark='+dirname+' \\\n')
        runHandle.write('\t--simpt-ckpt='+str(chkptNum)+' \\\n')

        runHandle.close()

        subprocess.call(["sed", "-i", "-e", 's|OUTDIR_REPLACE|%s|g' % outdir, runscriptFile])
        subprocess.call(["chmod", "+777", runscriptFile])
    

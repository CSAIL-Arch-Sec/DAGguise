import os
import sys
import subprocess
from shutil import copyfile
import numpy as np

weightarray = np.arange(0,400,10)
paraarray = [1,2,4,8]

gem5root = os.environ.get('GEM5_ROOT')
specroot = os.environ.get('SPEC_ROOT')

assert(gem5root is not None)
assert(specroot is not None)

for para in paraarray:
    for weight in weightarray:
        outdir = os.path.join(gem5root, "sensitivity", str(weight) + "_" + str(para)) 
        os.makedirs(outdir, exist_ok=True)

        runscriptFile = os.path.join(outdir, str(weight) + "_" + str(para) + "_runscript.sh") 
        copyfile(sys.argv[1], runscriptFile)

        runHandle = open(runscriptFile, "a+")

        dagName = os.path.join(outdir, str(weight) + "_" + str(para) + ".json")
        dramsim2File = os.path.join(outdir, str(weight) + "_" + str(para))

        subprocess.call(["python3", gem5root+"/dag_generator/dag_generator.py", \
                "--para=" + str(para), "--weight=" + str(weight), \
                "--outputfile=" + dagName])

        runHandle.write('\t--dagprotectionfile=' + dagName + '\\\n')
        runHandle.write('\t--dramsim2outputfile=%s \\\n' % (dramsim2File))

        runHandle.close()
        
        subprocess.call(["sed", "-i", "-e", 's|OUTDIR_REPLACE|%s|g' % outdir, runscriptFile])
        subprocess.call(["chmod", "+777", runscriptFile])

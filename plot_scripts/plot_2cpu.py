import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import csv
import re
from scipy import stats

gem5root = os.environ.get('GEM5_ROOT')
specroot = os.environ.get('SPEC_ROOT') 

assert(gem5root is not None)
assert(specroot is not None)


df = pd.DataFrame(columns = ["test", "chkptnum", "cpu0_ipc", "cpu1_ipc", "ticks"])
exprs = ['blender_r', 'cactuBSSN_r', 'cam4_r', 'deepsjeng_r', 'exchange2_r', 'fotonik3d_r', 'lbm_r', 'leela_r', 'nab_r', 'namd_r', 'povray_r','roms_r', 'wrf_r', 'x264_r', 'xz_r']

weightDict = dict()

if len(sys.argv) <= 2:
    print("Usage: plot_2cpu.py results_dir testname1 testname2 testname3")
    print("Example: plot_2cpu.py $GEM5_ROOT/eval_scripts/simu_condor/results/ docDist_2cpu_DAGguise docDist_2cpu_FSBTA docDist_2cpu_regular")
    exit(0)

resultsdir = sys.argv[1]

for trialName in sys.argv[2:]:
    for testName in next(os.walk(os.path.join(sys.argv[1], trialName)))[1]:
        if testName not in exprs: continue
        with open(os.path.join(specroot, 'ckpt', testName, 'results.weights')) as f:
            for line in f.readlines():
                weightDict[line.split(' ')[1].split('\n')[0]] = float(line.split(' ')[0])

        for checkpointNum in next(os.walk(os.path.join(resultsdir, trialName, testName)))[1]:
            procDict = dict()
            procDict["test"] = testName[:-2]
            if "DAGguise" in trialName: 
                procDict["trial"] = "DAGguise"
            elif "FSBTA" in trialName: 
                procDict["trial"] = "FS-BTA"
            else:
                procDict["trial"] = trialName
            procDict["chkptnum"] = checkpointNum
            procDict["weight"] = weightDict[checkpointNum]

            with open(os.path.join(resultsdir, trialName, testName, checkpointNum, 'stats.txt')) as f:
                for line in f.readlines():
                    if "system.switch_cpus_10.ipc" in line:
                        procDict["cpu0_ipc"] = float(re.split(r'[ ]+',line)[1])
                    if "system.switch_cpus_11.ipc" in line:
                        procDict["cpu1_ipc"] = float(re.split(r'[ ]+',line)[1])
                    elif "sim_ticks" in line:
                        procDict["ticks"] = int(re.split(r'[ ]+',line)[1])
            df = df.append(procDict, ignore_index=True)
    
            
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df)

print("=== IPC Stats ===\n")

# Drop any failed tests
failed = df[df.isna().any(axis=1)]
for index, row in failed.iterrows():
    print("Dropping %s, %s" % (row['test'], row['chkptnum']))
    df = df.drop(df[(df['test'] == row['test']) & (df['chkptnum'] == row['chkptnum'])].index)

g = df.groupby(['test','trial'], as_index=False)

df['cpu_0_ipc_wa'] = df.cpu0_ipc * df.weight
df['cpu_1_ipc_wa'] = df.cpu1_ipc * df.weight

ipc_0 = g.cpu_0_ipc_wa.sum()
ipc_1 = g.cpu_1_ipc_wa.sum()

def divide_by(g, name, denom_lvl):
    cols = [name]
    num = g[cols]
    
    denom = g.loc[g.trial==denom_lvl, cols].iloc[0]
    return num.divide(denom*2)

ipc_0["SPEC"] = ipc_0.groupby(['test']).apply(divide_by, name = "cpu_0_ipc_wa", denom_lvl = "docDist_2cpu_regular")
ipc_1["DocDist"] = ipc_1.groupby(['test']).apply(divide_by, name = "cpu_1_ipc_wa", denom_lvl = "docDist_2cpu_regular")

ipc = ipc_1.join(ipc_0.set_index(['test','trial']), on=['test','trial'])

print(ipc)

def plot_clustered_stacked(dfall, labels=None, title="multiple stacked bar plot",  H="/", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot.
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0].columns)
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)
    colors = ['gainsboro', 'dimgray']

    i = 0

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=1,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      edgecolor='black',
                      color='white',

                      **kwargs)  # make bar plots
        i += 1

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col) - 0.125)
                rect.set_hatch(H * int(j)*2) #edited part
                rect.set_width(1 / float(n_df + 1))
                rect.set_facecolor(colors[int(i / (n_col))])


    axe.set_xticks((np.arange(0, 2 * n_ind, 2) - 0.35 + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 30, ha="right")
    axe.set_ylabel("Average Normalized IPC")

    # Add invisible data to add another legend
    n=[]
    for i in range(n_df):
        n.append(axe.bar(0, 0, color=colors[i], edgecolor='black'))

    l1 = axe.legend(n, labels, loc='upper center', bbox_to_anchor=(0.225, 1.19), ncol = 2, columnspacing=0.3, handletextpad=0.2)
    if labels is not None:
        l2 = plt.legend(h[:n_col], l[:n_col], loc='upper center', bbox_to_anchor=(0.8, 1.19), ncol = 2, columnspacing=0.3, handletextpad=0.2)
        l2.legendHandles[0].set_facecolor('white')
        l2.legendHandles[1].set_facecolor('white')
    axe.add_artist(l1)
    return axe

df_list = []
trial_list = []
geo_list = []
for trialRow in sorted(df.trial.unique(),reverse=True):
    if "regular" in trialRow: continue

    geodict = dict()
    geodict["test"] = "geomean"
    geodict["DocDist"] = stats.gmean(ipc[ipc['trial'] == trialRow][['DocDist']])[0].astype(float)
    geodict["SPEC"] = stats.gmean(ipc[ipc['trial'] == trialRow][['SPEC']])[0].astype(float)

    print(trialRow)
    print(ipc[ipc['trial'] == trialRow][['test', 'DocDist', 'SPEC']].append(geodict, ignore_index=True).set_index('test'))

    df_list.append(ipc[ipc['trial'] == trialRow][['test', 'DocDist', 'SPEC']].append(geodict, ignore_index=True).set_index('test'))
    trial_list.append(trialRow)

# Then, just call :
plt.rcParams["figure.figsize"] = (6,2.75)
#plot_clustered_stacked(df_list, trial_list, cmap=plt.cm.gray, title="Average Normalized Speedup")
plot_clustered_stacked(df_list, trial_list, title="Average Normalized Speedup")


box = plt.axes().get_position()
plt.axes().set_position([box.x0, box.y0+0.125, box.width*1.1, box.height*0.85])

plt.savefig("2cpu.pdf")
plt.show()


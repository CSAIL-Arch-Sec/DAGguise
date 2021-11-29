import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import os
import csv
import re
from matplotlib.patches import Rectangle

gem5root = os.environ.get('GEM5_ROOT')
specroot = os.environ.get('SPEC_ROOT') 

assert(gem5root is not None)
assert(specroot is not None)

df = pd.DataFrame(columns = ["cycles", "weight", "para", "ipc", "insts", "total_nodes", "fake_reads", "fake_writes", "bandwidth"])
pd.set_option("display.max_rows", None, "display.max_columns", None)

df = df.astype({"fake_reads": int, 'total_nodes': int, 'insts': int})

for folder in next(os.path.join(gem5root, "sensitivity"))[1]:
    para = folder.split('_')[-1]
    weight = folder.split('_')[-2]
    if (weight == '0'): continue;

    procDict = dict()
    procDict["weight"] = weight
    procDict["para"] = para

    with open(folder+'/stats.txt') as f:
        for line in f.readlines():
            if "ipc " in line:
                procDict["ipc"] = float(re.split(r'[ ]+',line)[1])
            elif "committedInsts" in line:
                procDict["insts"] = int(re.split(r'[ ]+',line)[1])
            elif "system.switch_cpus_1.numCycles" in line:
                procDict["cycles"] = int(re.split(r'[ ]+',line)[1])

    with open(folder+'/%s_%s.vis' % (weight, para)) as f:
        for line in f.readlines():
            if "Final Defence" in line:
                procDict["total_nodes"] = int(re.split(r'[ ]+',line)[-1].split(',')[0])
            elif "Number of Fake Read" in line:
                procDict["fake_reads"] = int(re.split(r'[ ]+',line)[-1].split(',')[0])
            elif "Number of Fake Write" in line:
                procDict["fake_writes"] = int(re.split(r'[ ]+',line)[-1])
            elif "Aggregate Average Bandwidth" in line:
                procDict["bandwidth"] = float(re.split(r'[ ]+',line)[-1])
        
    #print(procDict)
    df = df.append(procDict, ignore_index=True) 
            

print(df)



print("=== Stats ===\n")

print(df)

df["fake_read_prop"] = df['fake_reads'].divide(df['total_nodes'])
df["norm_ipc"] = df.ipc / df[df['weight'] == "out"]["ipc"].item()

skipval = 2
markersize = 75


vals = df[df.weight != "out"]
vals = vals.astype({"weight": float, 'para': int, 'bandwidth': float})

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=[colors[0], colors[2], colors[3], colors[4]])

mpl.rcParams.update({'font.size': 11.5})

fig, axs = plt.subplots(1,3,figsize=(11.5,2.82))

mkr_dict = {1: 'x', 2: '+', 4: '.', 8: '*'}
for kind in mkr_dict:
    d = vals[vals["para"] == kind]
    axs[0].scatter(d.weight[1::skipval], d.norm_ipc[1::skipval], marker=mkr_dict[kind], label=kind, s=markersize)

axs[0].set_xlabel('Weight\n(a)')
axs[0].set_ylabel('Normalized IPC')
handles, labels = [(a + b) for a, b in zip(axs[0].get_legend_handles_labels(), axs[1].get_legend_handles_labels())]
print(handles)
legend = fig.legend(handles, labels, loc='center left', title="Number of\nParallel Sequences", bbox_to_anchor=(0, 0.5), ncol=1, fancybox=True, shadow=True)

plt.setp(legend.get_title(), multialignment='center')

for kind in mkr_dict:
    d = vals[vals["para"] == kind]
    axs[1].scatter(d.weight[1::skipval], d.bandwidth[1::skipval], marker=mkr_dict[kind], label=kind, s=markersize)

axs[1].set_ylabel('Avg. Allocated\nBandwidth (GB/s)')
axs[1].set_xlabel('Weight\n(b)')

axs[2].add_patch(Rectangle((2, 0.75), 2, 0.15, linewidth=1.5, facecolor='orange', edgecolor='b', fill=True, alpha=0.3, linestyle='dotted', zorder=-1))

for kind in mkr_dict:
    d = vals[vals["para"] == kind]
    axs[2].scatter(d.bandwidth[1::skipval*2], d.norm_ipc[1::skipval*2], marker=mkr_dict[kind], label=kind, s=markersize)

axs[2].set_ylabel('Normalized IPC')
axs[2].set_xlabel('Avg. Allocated Bandwidth (GB/s)\n(c)')


#axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), title="Number of Parallel Accesses",
#          ncol=4, fancybox=True, shadow=True)
plt.tight_layout()
box = axs[0].get_position()
axs[0].set_position([box.x0+0.15, box.y0-0.06, box.width*0.8, box.height])
axs[0].axhline(y=0.4, color='lightgrey', linestyle='dotted')
axs[0].axhline(y=0.6, color='lightgrey', linestyle='dotted')
axs[0].axhline(y=0.8, color='lightgrey', linestyle='dotted')
box = axs[1].get_position()
axs[1].set_position([box.x0+0.1, box.y0-0.06, box.width*0.8, box.height])
axs[1].axhline(y=2, color='lightgrey', linestyle='dotted')
axs[1].axhline(y=4, color='lightgrey', linestyle='dotted')
axs[1].axhline(y=6, color='lightgrey', linestyle='dotted')
box = axs[2].get_position()
axs[2].set_position([box.x0+0.05, box.y0-0.06, box.width*0.8, box.height])
axs[2].axhline(y=0.4, color='lightgrey', linestyle='dotted')
axs[2].axhline(y=0.6, color='lightgrey', linestyle='dotted')
axs[2].axhline(y=0.8, color='lightgrey', linestyle='dotted')

plt.show()

'''
vals.plot.scatter(x='weight', y='fake_read_prop', c='para', colormap='viridis')
plt.show()
'''

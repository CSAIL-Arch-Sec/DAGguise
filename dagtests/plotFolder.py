import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import csv
import re

df = pd.DataFrame(columns = ["test", "weight_slack", "node_slack", "ipc", "ticks", "Defence_Nodes_Executed", "Fake_Read_Requests", "Fake_Write_Requests", "Fixed_Rate_Requests", "Fake_Fixed_Rate_Read_Requests", "Fake_Fixed_Rate_Write_Requests"])

for testName in os.listdir(sys.argv[1]):
    procDict = dict()
    procDict["test"] = testName
    if (testName != "reg" and testName != "fsb"):
        procDict["weight_slack"] = int(testName.split('W')[0])
        procDict["node_slack"] = int(testName.split('W')[1].split('N')[0])
    with open(sys.argv[1] + '/' + testName + '/m5out/stats.txt') as f:
        for line in f.readlines():
            if "system.cpu.ipc" in line:
                procDict["ipc"] = float(re.split(r'[ ]+',line)[1])
            elif "sim_ticks" in line:
                procDict["ticks"] = int(re.split(r'[ ]+',line)[1])
    
    with open(sys.argv[1] + '/' + testName + '/results/DDR3_micron_32M_8B_x8_sg125/4GB.1Ch.8R.scheme2.close_page.32TQ.32CQ.RtB.pRankpBank.vis') as f:
        for line in f.readlines():
            if "Final Defence Nodes Executed" in line:
                procDict["Defence_Nodes_Executed"] = int(line.split(': ')[1].split(',')[0])
            elif "Number of Fake Read Requests" in line:
                procDict["Fake_Read_Requests"] = int(line.split(': ')[1].split(',')[0])
            elif "Number of Fake Write Requests" in line:
                procDict["Fake_Write_Requests"] = int(line.split(': ')[1].split(',')[0])
            elif "Fixed Rate Requests" in line:
                procDict["Fixed_Rate_Requests"] = int(line.split(': ')[1].split(',')[0])
            elif "Fixed Rate Fake Read Requests" in line:
                procDict["Fake_Fixed_Rate_Read_Requests"] = int(line.split(': ')[1].split(',')[0])
            elif "Fixed Rate Fake Write Requests" in line:
                procDict["Fake_Fixed_Rate_Write_Requests"] = int(line.split(': ')[1])

    print(procDict)
    df = df.append(procDict, ignore_index=True)

print(df)

dagExamples = df[("reg" != df['test']) & ("fsb" != df['test'])]
print(dagExamples)

plt.rcParams["figure.figsize"] = (8,4.5)

weightSkew = dagExamples[(dagExamples['node_slack'] == 0)]
nodeSkew = dagExamples[(dagExamples['weight_slack'] == 0)]

weightSkew.sort_values('weight_slack', ascending=False).plot.line(x='weight_slack', y='ticks')
plt.title("Execution Time for Differing Weight Slacks")
plt.ylabel("Ticks")
plt.xlabel("Weight Slack")

plt.show()

nodeSkew.sort_values('node_slack', ascending=False).plot.line(x='node_slack', y='ticks')
plt.title("Execution Time for Differing Node Slacks")
plt.ylabel("Ticks")
plt.xlabel("Node Slack")

plt.show()

'''

df["Associativity"] = df["Associativity"].astype(int)
df["Block Size (B)"] = df["Block Size (B)"].astype(int)
df["Num Rows"] = df["Num Rows"].astype(int)
df["Cache Size (B)"] = df["Cache Size (B)"].astype(int)

os.makedirs("figures/", exist_ok=True)
plt.tight_layout()

pipt_df = df["physical index physical tag" == df['type']]

assoc_pipt = pipt_df[pipt_df.config.isin(["b2_r6_a8", "b2_r7_a4", "b2_r8_a2", "b2_r9_a1"])]
print(assoc_pipt[assoc_pipt.test.isin(["bzip2"])])
plt.rcParams["figure.figsize"] = (8,4.5)
assoc_pipt.pivot("Test Name", "Associativity", "readHitRate").plot(kind='bar')
plt.title("Associativity Variations (Read Hit Rate, 4B Blocks, 2KB Cache)")
plt.ylabel("Read Hit Rate")
plt.savefig("figures/q1_assoc_read.png")
'''

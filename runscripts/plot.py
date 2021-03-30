import sys
import array
import warnings
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

try:
    fp = open("test.out", 'r')
    tick_fp = open("m5out/stats.txt", 'r')
except:
    print "Usage: python %s <timings.bin>" % (sys.argv[0])
    sys.exit(1)

out = fp.readlines()
out_tick = tick_fp.readlines()

first = 0
last = 0

for line in out_tick:
    if "final_tick" in line:
        if first == 0:
            first = int(line.split()[1])
        elif last == 0:
            last = int(line.split()[1])

x = []
total = []
init = []
final = []
wait = []

print(first)
print(last)

for line in out:
    if "Addr" in line:
        if "dcache" in line:
            if "cpu0" in line:
                if int(line.split(':')[0]) < last and int(line.split(':')[0]) > first:
                    x.append(int(line.split(':')[0]))
                    total.append((int(line.split(':')[0]) - int(line.split(':')[5]))/1000)
                    final.append((int(line.split(':')[0]) - int(line.split(':')[7]))/1000)
                    wait.append((int(line.split(':')[7]) - int(line.split(':')[5]))/1000)

print(len(total))

plt.title('Dependent Transmitter - End-to-End MSHR Latency')
plt.ylabel('Miss Latency')
plt.xlabel('Simulation Cycle')
plt.plot(x,total,'.')

plt.figure()
plt.title('Dependent Transmitter - MSHR to Head of Read Queue Latency')
plt.ylabel('Miss Latency')
plt.xlabel('Simulation Cycle ')
plt.plot(x,wait,'.')

plt.show()

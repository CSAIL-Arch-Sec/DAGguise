
import sys, random
random.seed(0)


NUM_OUTPUT = 1
NUM_GENE = 2000


with open(sys.argv[1]) as f:
  lines = f.readlines()

geneTotal = int(len(lines) / 4) - 1 # last line may not have \n
candidate = []
for _ in range(NUM_OUTPUT):
  temp = []
  for _ in range(NUM_GENE):
    temp.append(random.randint(0, geneTotal))
  candidate.append(temp)


for i, geneIndexList in enumerate(candidate):
  with open(sys.argv[1][:-3] + "_%d-%d.fq"%(NUM_GENE, i), "w") as f:
    for geneIndex in geneIndexList:
      f.writelines(lines[4*geneIndex])
      f.writelines(lines[4*geneIndex + 1])
      f.writelines(lines[4*geneIndex + 2])
      f.writelines(lines[4*geneIndex + 3])


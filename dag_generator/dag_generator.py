#!/usr/bin/env python

import sys, argparse, json

# Gather our code in a main() function
def main(args):

  numPhase = args.numphase
  numPara = args.para
  wbRatio = args.wbratio
  latency = args.weight
  numBanks = args.numbanks

  node = []
  edge = []

  # start node
  node.append({"nodeID": 0, "bankID": 0, "combinedWB": 1, "combinedWBBankID": 0}) 
  # main node
  for phaseID in range(numPhase):
    for paraID in range(numPara):
      nodeID = phaseID*numPara + paraID + 1 
      node.append({"nodeID": nodeID, "bankID": nodeID%numBanks, "combinedWB": \
              int(phaseID % wbRatio == 0), "combinedWBBankID": nodeID%numBanks})
  # end node
  node.append({"nodeID": numPhase*numPara+1, "bankID": 0, "combinedWB": 1, "combinedWBBankID": 0}) 

  # start edge
  for paraID in range(numPara):
    edge.append({"sourceID": 0, "destID": paraID+1, "latency": latency})
  # main edge
  for phaseID in range(numPhase-1):
    for paraID in range(numPara):
      nodeID0 = phaseID*numPara + paraID + 1
      nodeID1 = (phaseID+1)*numPara + paraID + 1
      edge.append({"sourceID": nodeID0, "destID": nodeID1, "latency": latency})
  # end edge
  for paraID in range(numPara):
    edge.append({"sourceID": numPhase*numPara-paraID, "destID": numPhase*numPara+1, "latency": latency})

  finalJson = {"0": {"loop": 100, "node": node, "edge": edge}}

  with open(args.outputfile, 'w') as json_file:
      json.dump(finalJson, json_file, indent=4)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description = "Generates defense rDAGs according to the template shown in Figure 6")
  parser.add_argument(
                      "--para",
                      type = int,
                      default = 8,
                      help = "rDAG Parallelism"
                      )

  parser.add_argument(
                      "--weight",
                      type = int,
                      default = 100,
                      help = "Edge Weight")

  parser.add_argument(
                      "--wbratio",
                      type = int,
                      default = 11,
                      help = "How many phases should we go before writing?")
  
  parser.add_argument(
                      "--numphase",
                      type = int,
                      default = 100,
                      help = "Number of Phases")
  
  parser.add_argument(
                      "--numbanks",
                      type = int,
                      default = 8,
                      help = "Number of DRAM Banks")
  
  parser.add_argument(
                      "--outputfile",
                      type = str,
                      default = "defense.json",
                      help = "DAG output file name")

  args = parser.parse_args()
  
  main(args)

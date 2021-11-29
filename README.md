## DAGguise 

This is the official performance demonstration for the DAGguise shaper system, as
first described in *DAGguise: Mitigating Memory Timing Side Channels*.

## Repository Overview

This main repository contains a modified fork (last commit in Februrary 2020) of the modified gem5 simulator. Apart from miscellaneous glue logic, all changes pertinent to the DAGguise shaper are contained in the DRAMSim2 submodule.

All necessary scripts for evaluation are stored in *eval_scripts/*. Other important folders include:

 - **checkpoint/** - Generation and storage of single-CPU checkpoints (for victim programs)
 - **checkpoint_merge/** - Generation and storage of multi-CPU checkpoints (for combining executions of SPEC and victim programs on different cores)
 - **dag_generator/** - A tool for generating rDAGs
 - **docker/** - Necessary files to run the simulation in a containerized Docker environment
 - **sample_programs/** - Containing the source code and Makefiles for sample victim programs (ex. DocDist and DNA)

## Cloning
Clone the DAGguise repository with *--recurse-submodules* to also get the DRAMSim2 implementation. 
## Setup and Execution

We include an example workflow to replicate Figure 9 (two-core IPC) in \texttt{eval\_scripts/}. 

The scripts perform the following tasks:

  - run\_once.sh - Patches the user-provided SPEC2017 gem5
  checkpoints to be compatible with the provided version of gem5 (this only should be run once).
  - build\_gem5.sh - Builds gem5 using the standard SCons workflow
  - generate\_sample\_checkpoints.sh - Builds DocDist (the sample victim program) and generates a standalone checkpoint.
  - merge\_checkpoint.sh - Merges the single CPU checkpoints of DocDist and each SPEC simpoint checkpoint into a new `combined' checkpoint (used for 2 CPU simulation) .
  - generate\_dag.sh - Generates a sample defense rDAG
  - run\_simu.sh - Executes the merged SPEC/DocDist checkpoint under the simulator framework.
  - plot\_results.sh - Plots the results shown in Figure 7.

Some scripts are are split into \_single and \_condor variants. The \_single scripts are used to execute a single
Simpoint/DocDist execution pair, while \_condor scripts are used for
batch execution. For Figure 7, approximately 150 runs must be executed (10
simpoints * 15 benchmarks).


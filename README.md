## DAGguise 

This is the official performance demonstration for the DAGguise shaper system, as
first described in *DAGguise: Mitigating Memory Timing Side Channels*.

## Repository Overview

This main repository contains a modified fork (last commit in Februrary 2020) of the modified gem5 simulator. Apart from miscellaneous glue logic, all changes pertinent to the DAGguise shaper are contained in the DRAMSim2 submodule.

All necessary scripts for evaluation are stored in *eval_scripts/*, as described in the paper's artifact abstract. Other important folders include:

 - **checkpoint/** - Generation and storage of single-CPU checkpoints (for victim programs)
 - **checkpoint_merge/** - Generation and storage of multi-CPU checkpoints (for combining executions of SPEC and victim programs on different cores)
 - **dag_generator/** - A tool for generating rDAGs
 - **docker/** - Necessary files to run the simulation in a containerized Docker environment
 - **sample_programs/** - Containing the source code and Makefiles for sample victim programs (ex. DocDist and DNA)

## Cloning
Clone the DAGguise repository with *--recurse-submodules* to also get the DRAMSim2 implementation. 

## Setup 
The DAGguise platform has the same baseline dependencies as [gem5](https://www.gem5.org/documentation/general_docs/building). Once these dependencies are installed, the rest of the simulator build is handled by the provided workflow (described in "Execution").

## Single vs Batch Experiments
DAGguise is executed similarly to baseline gem5, simply requiring additional parameter inputs (such as the DRAM protection policy, and defense rDAG if applicable). Example execution scripts to launch a single instance of a DAGguise simulation exist in the \texttt{eval\_scripts/} folder under the \texttt{\_single} suffix. 

To perform rDAG sensitivity analysis (or to replicate the paper's figures, which require upwards of 500 individual simulator runs), HTCondor *must* be used. HTCondor is an unix-compatible open-source job management tool, allowing for the convenient parallelization of many DAGguise instances. We provide condor-compatible launch scripts in the \texttt{eval\_scripts/} folder under the \texttt{\_condor} suffix.

If you do not already have access to an HTCondor cluster, we highly recommend installing HTCondor under the default ["minihtcondor" configuration](https://htcondor.readthedocs.io/en/latest/getting-htcondor/install-linux-as-root.html). It is recommended (but not required) that the machine has 48+ cores in order to speed up parallelization and reduce total simulation time.

### HTCondor Tips + Quirks

- To observe the HTCondor job status, use *condor_q*. If jobs are in the "held" state, use *condor_q --better-analyse* to determine the reason. To kill outstanding condor batch jobs, use *condor_rm <batch_id>*.
- If jobs are finishing very fast (and not generating any output), check the job error files generated by HTCondor (generated in the folder where the job is launched, which is not necessarily the current directory).
  - If you're experiencing *permission denied* errors, ensure that the HTCondor *user* has read/write permissions to the files being touched during simulation. The easiest way to do this is recursively set +777 permissions on all files in the DAGguise folder (+ SPEC benchmarks folder, if applicable) using *chmod +777 -R DAGguise* (please understand the security implications of this before doing this though!).
  - If you're experiencing *file not found* errors and are running on a HTCondor cluster which spans multiple machines, ensure that the DAGguise folder is stored on a file system which is *shared* between all machines in the cluster. If a shared filesystem is unavailable it is also possible to use HTCondor's built in [file transfer mechanism](https://htcondor.readthedocs.io/en/latest/users-manual/file-transfer.html), however we do not provide scripts to use this functionality.

## Execution
We include an example workflow to replicate Figure 7 (Offline Profiling) and Figure 9 (two-core IPC) in \texttt{eval\_scripts/}. 

The scripts perform the following tasks:

  - run\_once.sh - Patches the user-provided SPEC2017 gem5 checkpoints to be compatible with the provided version of gem5 (this only should be run once).
  - build\_gem5.sh - Builds gem5 using the standard SCons workflow.
  - generate\_sample\_checkpoints.sh - Builds DocDist (the sample victim program) and generates a standalone checkpoint.
  - merge\_checkpoint.sh - Merges the single CPU checkpoints of DocDist and each SPEC simpoint checkpoint into a new `combined' checkpoint (used for 2 CPU simulation).
  - generate\_dag.sh - Generates a sample defense rDAG
  - run\_simu.sh - Executes the merged SPEC/DocDist checkpoint(s) under the simulator framework.
  - plot\_fig9.sh - Plots the results shown in Figure 9.
  - run\_sensitivity\_condor.sh - Runs the defense rDAG parameter sweep (i.e. the offline profiling step, described in Section 4.3).
  - plot\_fig7.sh - Plots the results shown in Figure 7.

Some scripts are are split into \_single and \_condor variants. The \_single scripts are used to execute a single
Simpoint/DocDist execution pair, while \_condor scripts are used for
batch execution.

### Other Execution Tips + Notes
- Ensure that $GEM5_ROOT (and $SPEC_ROOT, if applicable) are properly exported before running the flow
- Using checkpoints is not strictly necessary to evaluate DAGguise on your own applications, they are used in our flow to ensure that the main ROI of each of our victim program is reached. Checkpoints are generated in an [unchanged manner compared to baseline gem5](https://www.gem5.org/documentation/general_docs/checkpoints/).
- Due to limitations with the version of Gem5 used, both Python 2 and 3 must be installed on the system (Python 3 being used for the vast majority of scripts, while Python 2 is used to perform the checkpoint merge step). The included evaluation scripts explicitly run python2 when it is required.
- Depending on minor variations in Gem5 behaviour, the evaluation script for step 4 (merge\_checkpoint) may need to be updated to point to the correct output folder generated by step 3 (i.e. the checkpoint tick number may vary slightly). 
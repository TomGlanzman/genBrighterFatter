# genBrighterFatter
Workflows to generate LSST brighter-fatter kernels

There are two branches to this repo: 'bash' is a bash-based workflow
to generate brighter-fatter kernels, while "Parsl" is parsl-based.


=====================================================


## bash version

Note: this is intended to be a temporary stop-gap used to validate the
DM setup and generation of BF kernels, and to create them while the
parsl version is developed.

Instructions for running the scripts are located in the README.txt file.

Directory structure after a bash-based kernel generation run:
```
|-- README.txt
|-- bfFlatVisits.txt
|-- block1.log
|-- block2.log
|-- block3.log
|-- block4.log
|-- block5.log
|-- block6.log
|-- configTask.sh
|-- cvmfsSetup.sh
|-- fullFP-1.sh
|-- fullFP-2.sh
|-- genBFkernel.sh
|-- initRepo.log
|-- initRepo.sh
|-- oneSensor.sh
|-- runInit.sh
|-- single.sh
|-- single1.log
```


=====================================================


## PARSL version

The current design of the Parsl prototype task is as follows:

```
runInit.sh                  - driver to set up environment and run the 
   |                                repository initialization (performed only 
   |				    once per repo)
   |
   +- configTask.sh  - task-specific config expressed as env-vars
   |
   +- cvmfsSetup.sh - DM setup
   |
   +- initRepo.sh       - Create and populate DM-style repository

------------

runWorkflow.sh	   - driver to establish environment and run the BF kernel 
   |                                 generator via Parsl
   |
   +- configTask.sh
   |
   +- cvmfsSetup.sh
   |
   +- BFworkflow.py	- top-level Parsl script: define and execute user script
            |
            + (pConfig.py )  - import customized Parsl configuration
            |
	    + N  x  genBF("genBFkernel.sh")   - organize options and call BF kernel code
		    |		|                                        (a parsl "bash_app")
		    |		|
		    |	       +- makeBrighterFatterKernel.py  - DM code
		    |
		    +- <Parsl distributes processing per "Config">
```
---------------------------------------------------------------------------------------------------------

The directory structure looks something like this, during the 64th attempt to run a workflow (run 063).  This workflow processes all 189 sensors and utilizes three Cori-KNL nodes with 32 workers per node (i.e., with 32 instances of makeBrighterFatterKernel.py running on each node).

```
|-- BFworkflow.py
|-- bfFlatVisits.txt
|-- configTask.sh
|-- cvmfsSetup.sh
|-- genBFkernel.sh
|-- initRepo.log.gz
|-- initRepo.sh
|-- monitoring.db
|-- pConfig.py
|-- runInit.sh
|-- runWorkflow.sh
|-- runinfo
|   |-- 000
|   |
       [...]
|   |
|   `-- 063
|       |-- checkpoint
|       |   |-- dfk.pkl
|       |   `-- tasks.pkl
|       |-- coriBatchM
|       |   |-- 3f81c2f199a4
|       |   |   |-- manager.log
|       |   |   |-- worker_0.log
|       |   |   |-- worker_1.log
|       |   |   |-- worker_10.log
   [...]
|       |   |   |-- worker_8.log
|       |   |   `-- worker_9.log
|       |   |-- 5bfee5402840
|       |   |   |-- manager.log
|       |   |   |-- worker_0.log
|       |   |   |-- worker_1.log
|       |   |   |-- worker_10.log
   [...]
|       |   |   |-- worker_8.log
|       |   |   `-- worker_9.log
|       |   |-- aa4dcbfe6854
|       |   |   |-- manager.log
|       |   |   |-- worker_0.log
|       |   |   |-- worker_1.log
   [...]
|       |   |   |-- worker_8.log
|       |   |   `-- worker_9.log
|       |   `-- interchange.log
|       |-- database_manager.log
|       |-- hub.log
|       |-- monitoring_hub.log
|       |-- parsl.log
|       |-- submit_scripts
|       |   |-- parsl.auto.1561052815.3880541.submit
|       |   |-- parsl.auto.1561052815.3880541.submit.stderr
|       |   `-- parsl.auto.1561052815.3880541.submit.stdout
|       `-- task_logs
|           `-- 0000
|               |-- task_0000_genBF_makeMBF.stderr
|               |-- task_0000_genBF_makeMBF.stdout
|               |-- task_0001_genBF_makeMBF.stderr
|               |-- task_0001_genBF_makeMBF.stdout
   [...]
|               |-- task_0187_genBF_makeMBF.stdout
|               |-- task_0188_genBF_makeMBF.stderr
|               `-- task_0188_genBF_makeMBF.stdout
```

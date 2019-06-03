# genBrighterFatter
Workflows to generate LSST brighter-fatter kernels

There are two branches to this repo: 'bash' is a script-based workflow
to generate brighter-fatter kernels, while "Parsl" is parsl-based.


## bash version

Note: this is intended to be a temporary stop-gap used to validate the
DM setup and generation of BF kernels, and to create them while the
parsl version is developed.

Instructions for running the scripts are located in the README.txt file.

Directory structure after a kernel generation run:
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
   |                                repository initialization
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

The directory structure looks something like this, during the 44th attempt to run a workflow:

```
.
|-- BFworkflow.py                top-level Parsl script
|-- Kernel1.log			 stdout log from one of five "workers" (instances of makeBrighterFatterKernel.py) 
|-- Kernel2.log
|-- Kernel3.log
|-- Kernel4.log
|-- Kernel5.log
|-- KernelErr1.log		stderr log from one of five "workers"
|-- KernelErr2.log
|-- KernelErr3.log
|-- KernelErr4.log
|-- KernelErr5.log
|-- configTask.sh		workflow-specific configuration
|-- cvmfsSetup.sh		DM-specific configuration
|-- dbtest3.py			simple monitoring report generator
|-- genBFkernel.sh		call the DM code
|-- initRepo.sh			initialize a DM repo in preparation for generating BF kernels
|-- monitoring.db		Parsl monitoring database
|-- pConfig.py			Parsl-specific configuration
|-- runInit.sh			Establish environment then call initRepo.sh
|-- runWorkflow.sh		Establish environment then call BFworkflow.py
|-- runinfo				Directory structure created and managed by Parsl
|   |-- 000
[...]
|   `-- 044				All the logs and scripts you could want (from Parsl)
|       |-- coriHinteractive
|       |   |-- bfea0e1824d3
|       |   |   |-- manager.log
|       |   |   |-- worker_0.log
|       |   |   |-- worker_1.log
|       |   |   |-- worker_2.log
|       |   |   |-- worker_3.log
|       |   |   `-- worker_4.log
|       |   `-- interchange.log
|       |-- database_manager.log
|       |-- hub.log
|       |-- monitoring_hub.log
|       |-- parsl.log
|       `-- submit_scripts
|           `-- parsl.auto.1559335572.885816.sh
`-- status				Simple script to monitor SLURM jobs
```

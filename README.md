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


=====================================================
=====================================================
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
   +- BFworkflow.py	- top-level Parsl script; define parsl.Config; define user 
            |		  	    	  script; execute user script
            |
	    + N x   genBF("genBFkernel.sh")   - organize options and call BF kernel code
		    |		|                                        (a parsl "bash_app")
		    |		|
		    |	       +- makeBrighterFatterKernel.py  - DM code
		    |
		    +- <Parsl distributes processing per "Config">
```
---------------------------------------------------------------------------------------------------------

The directory structure looks like this, after two "runs" of the top-level workflow script:

```
.
|-- BFworkflow.py                                         
|-- README.txt                                            
|-- bfFlatVisits.txt                                      
|-- configTask.sh                                         
|-- cvmfsSetup.sh
|-- initRepo.sh
|-- runInit.sh
|-- runWorkflow.sh
|-- runinfo
|   |-- 000
|   |   |-- cori_haswell
|   |   |   |-- 62ad56bf247d
|   |   |   |   |-- manager.log
|   |   |   |   `-- worker_0.log
|   |   |   `-- interchange.log
|   |   |-- parsl.log
|   |   `-- submit_scripts
|   |       |-- parsl.auto.1554160602.4217892.submit
|   |       |-- parsl.auto.1554160602.4217892.submit.stderr
|   |       `-- parsl.auto.1554160602.4217892.submit.stdout
|   `-- 001
|       |-- cori_haswell
|       |   |-- e9ce0f8773d2
|       |   |   |-- manager.log
|       |   |   `-- worker_0.log
|       |   `-- interchange.log
|       |-- parsl.log
|       `-- submit_scripts
|           |-- parsl.auto.1554163736.7880213.submit
|           |-- parsl.auto.1554163736.7880213.submit.stderr
|           `-- parsl.auto.1554163736.7880213.submit.stdout
|-- stderr.log
`-- stdout.log
```

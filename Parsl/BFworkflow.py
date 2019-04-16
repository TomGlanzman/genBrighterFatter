# BFworkflow.py - top-level Parsl workflow script
#
# One must first have the proper environment (with parsl) to run this scrupt.

import os,sys,datetime

startTime = datetime.datetime.now()
print(startTime, ": Entering BFworkflow.py")


import parsl
from parsl.app.app    import  python_app, bash_app
from parsl.providers  import  SlurmProvider
from parsl.channels   import  LocalChannel
from parsl.launchers  import  SingleNodeLauncher
from parsl.executors  import  HighThroughputExecutor
from parsl.config     import  Config

## New Parsl monitoring (since v0.7.2)
from parsl.monitoring.monitoring import MonitoringHub
from parsl.addresses import address_by_hostname
import logging

## Parsl checkpointing




print("parsl version = ",parsl.__version__)

## Configure the brighter-fatter 'task'

## candidate SLURM stuff
#SBATCH -q regular        #Select partition, e.g. regular,premium,interactive
#SBATCH -N 1                 #Number of full cori nodes to occupy
#SBATCH -t 00:05:00      #Set runtime limit (see queues/policies page for max limits)
#SBATCH -L SCRATCH,projecta    #Job requires $SCRATCH file system
#SBATCH -C knl              # user knl nodes
##SBATCH -C haswell    # user haswell nodes
#DW persistentdw name=Run20p  # burst buffer


##
## Values used by all steps in this workflow
workflowRoot = os.environ['PT_WORKFLOWROOT']


##
## Configure Parsl execution of the BF kernel generation step
hostName = os.environ['HOSTNAME']

config = Config(
    app_cache=True, 
    checkpoint_files=None, 
    checkpoint_mode='dfk_exit', 
    checkpoint_period=None, 
    executors=[
        HighThroughputExecutor(
            label='cori-1',
            address=hostName,   # node upon which the top-level parsl script is running
            cores_per_worker=os.environ['PT_CORESPERSTEP'],     # Single-threaded
            max_workers=int(os.environ['PT_JOBSPERNODE']),           # user jobs/node
            poll_period=30,
            provider=SlurmProvider(
                partition=os.environ['PT_QUEUE'],               # SLURM job "queue"
                walltime=os.environ['PT_WALLTIME'],
                cmd_timeout=90,                # Extend time waited in response to 'sbatch' command
                nodes_per_block=int(os.environ['PT_NODESPERJOB']),   # Nodes per batch job
                init_blocks=int(os.environ['PT_INITJOBS']),
                min_blocks=int(os.environ['PT_MINJOBS']),       # limits on batch job requests
                max_blocks=int(os.environ['PT_MAXJOBS']),
                parallelism=0.1,            # reduce "extra" batch jobs
                scheduler_options=os.environ['PT_BATCHOPTS'],
                worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
                channel=LocalChannel(),    # batch communication is performed on this local machine
                launcher=SingleNodeLauncher(),
            ),
        ),
        HighThroughputExecutor(
            label='cori-2',
            address=hostName,   # node upon which the top-level parsl script is running
            cores_per_worker=2,   # threads per user job
            max_workers=4,           # user jobs/node
            poll_period=30,
            provider=SlurmProvider(
                partition='debug',               # SLURM job "queue"
                walltime='00:30:00',
                cmd_timeout=90,                # Extend time waited in response to 'sbatch' command
                nodes_per_block=1,   # Nodes per batch job
                init_blocks=0,
                min_blocks=1,                  # limits on batch job requests
                max_blocks=1,
                parallelism=0.1,            # reduce "extra" batch jobs
                scheduler_options="#SBATCH -L SCRATCH,projecta \n#SBATCH --constraint=haswell",
                worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
                channel=LocalChannel(),    # batch communication is performed on this local machine
                launcher=SingleNodeLauncher(),
            ),
        )
    ],
    monitoring=MonitoringHub(
        hub_address=address_by_hostname(),
        hub_port=55055,
        logging_level=logging.INFO,
        resource_monitoring_interval=60,
    ),
)

print(datetime.datetime.now(), ": Parsl configuration setup complete")
print("config = ",config)
parsl.load(config)
print(datetime.datetime.now(), ": Parsl config complete!")

## Define workflow steps


@bash_app(executors=['cori-1'])
def genBFk(cmd, stdout='stdout.log', stderr='stderr.log'):
    ## Command executor - intended for BF kernel generation
    import os,sys,datetime
    print(datetime.datetime.now(),' Entering genBF')
    return f'{cmd}'

@bash_app(executors=['cori-2'])
def genBFh(cmd, stdout='stdout.log', stderr='stderr.log'):
    ## Command executor - intended for BF kernel generation
    import os,sys,datetime
    print(datetime.datetime.now(),' Entering genBF')
    return f'{cmd}'

## Submit and Run the workflow steps
print(datetime.datetime.now(), ": Run BF generation")

#/usr/bin/time -v ./genBFkernel.sh   0  39 ${PT_RERUNDIR}1 40 |tee ${PT_RERUNDIR}1.log
timex = "/usr/bin/time -v "

## Define list of sensors for which to calculate BF kernel
sensorList = [27,93,94,187]

## Submit parsl job steps
jobsk = []
jobsh = []
njobs = 0
for sensor in sensorList:
    njobs += 1
    cmd = workflowRoot+"/genBFkernel.sh "+str(sensor)+" "+str(sensor)+" "+os.environ['PT_RERUNDIR']+ " 1"
    print('cmd = ',cmd)
    stdo = 'Kernel'+str(njobs)+'.log'
    stde = 'KernelErr'+str(njobs)+'.log'
    if njobs < 0:
        print("Creating KNL task ",njobs-1)
        jobsk.append(genBFk(cmd,stdout=stdo,stderr=stde))
    else:
        print("Creating Haswell task ",njobs-1)
        jobsh.append(genBFh(cmd,stdout=stdo,stderr=stde))
        pass
    pass
print(" Total number of parsl tasks created = ",njobs)




## Introspect the parsl tasks
#print("Workflow info:")
#print("type(parsl) = ",type(parsl))
#print("dir(parsl) = ",dir(parsl))

#print("type(jobsk[0]) = ",type(jobsk[0]))
#print("dir(jobsk[0]) = ",dir(jobsk[0]))


## Uncomment the assert if running with "python -i"
#assert False,"Entering python interpreter"



## Wait for jobs to complete

print("Begin waiting for defined tasks to complete...")
try:
    parsl.wait_for_current_tasks()
except:         # Unhandled exception will cause script to abort
    print("Exception!  parsl.wait_for_current_tasks()   Bah!")
pass


print("Check return code for each task")
### Can the .result() function also cause an exception???
jobn = 0
try:
    for job in jobsh:
        print("waiting for Haswell job ",jobn)
        print("rc = ",job.result())
        jobn += 1
        pass
    for job in jobsk:
        print("waiting for KNL job ",jobn)
        print("rc = ",job.result())
        jobn += 1
        pass
except:
    print("Exception waiting for job ",jobn)
    pass



## Final bookkeeping
endTime = datetime.datetime.now()
elapsedTime = endTime-startTime
print("Time to complete BF generation = ",elapsedTime)
print(endTime,": Exiting BFworkflow")

#sys.exit()





## pConfig.py - python3 module to create a Parsl configuration for use in a top-level workflow script

##  To use this file, create the desired executor(s), giving each a
##  unique name.  Activate the needed executors at the *end* of this
##  file in the "Config" object.  Note that each activated executor
##  has some associated overhead so it is recommended to activate only
##  those you will use.

## T.Glanzman - May 2019

##
## import all needed Parsl elements
##

import sys,os,logging
import parsl
from parsl.providers  import  SlurmProvider
from parsl.providers  import  LocalProvider
from parsl.channels   import  LocalChannel
from parsl.launchers  import  SingleNodeLauncher
from parsl.launchers  import  SrunLauncher
from parsl.launchers  import  SimpleLauncher
from parsl.executors  import  HighThroughputExecutor
from parsl.executors  import  ThreadPoolExecutor
from parsl.config       import  Config

## Parsl monitoring
from parsl.monitoring.monitoring import MonitoringHub
from parsl.addresses import address_by_hostname


##
##   Configure Parsl
##
hostName = address_by_hostname()
#print('Running on node determined by parsl: ',hostName)


##
##  Define Parsl executors
##

## This executor is intended for large-scale batch work with *multiple* nodes & workers/node
coriBatchM = HighThroughputExecutor(
    label='coriBatchM',
    address=address_by_hostname(),  # node upon which the top-level parsl script is running
    cores_per_worker=1,        # threads per user job
    max_workers=32,            # user tasks/node
    poll_period=30,
    provider=SlurmProvider(          # Dispatch tasks via SLURM
        partition='regular',               # SLURM job "queue"
        walltime='08:00:00',
        cmd_timeout=90,                # Extend time waited in response to 'sbatch' command
        nodes_per_block=3,      # Nodes per batch job
        init_blocks=0,                # of batch jobs to submit in anticipation of future demand
        min_blocks=1,               # limits on batch job requests
        max_blocks=1, 
        parallelism=0.1,            # reduce "extra" batch jobs
        scheduler_options="#SBATCH -L SCRATCH,projecta \n#SBATCH --constraint=knl",
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
        channel=LocalChannel(),    # batch communication is performed on this local machine
        launcher=SrunLauncher()
    ),
)


## This executor is intended for batch work on a *single* KNL node with multiple workers
coriBatch1 = HighThroughputExecutor(
    label='coriBatch1',
    address=address_by_hostname(),  # node upon which the top-level parsl script is running
    cores_per_worker=1,        # threads per user job
    max_workers=30,            # user tasks/node
    poll_period=30,
    provider=SlurmProvider(          # Dispatch tasks via SLURM
        partition='regular',               # SLURM job "queue"
        walltime='08:00:00',
        cmd_timeout=90,                # Extend time waited in response to 'sbatch' command
        nodes_per_block=1,      # Nodes per batch job
        init_blocks=0,                # of batch jobs to submit in anticipation of future demand
        min_blocks=1,               # limits on batch job requests
#        max_blocks=4,              # max batch jobs
        max_blocks=1,              # max batch jobs
        parallelism=0.1,            # reduce "extra" batch jobs
        scheduler_options="#SBATCH -L SCRATCH,projecta \n#SBATCH --constraint=knl",
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
        channel=LocalChannel(),    # batch communication is performed on this local machine
        launcher=SingleNodeLauncher()
    ),
)

## This executor is intended for batch work on a single Haswell node with multiple workers
coriHBatch1 = HighThroughputExecutor(
    label='coriHBatch1',
    address=address_by_hostname(),  # node upon which the top-level parsl script is running
    cores_per_worker=1,        # threads per user job
    max_workers=40,            # user tasks/node
    poll_period=30,
    provider=SlurmProvider(          # Dispatch tasks via SLURM
        partition='regular',               # SLURM job "queue"
        walltime='01:30:00',
        cmd_timeout=90,                # Extend time waited in response to 'sbatch' command
        nodes_per_block=1,      # Nodes per batch job
        init_blocks=0,                # of batch jobs to submit in anticipation of future demand
        min_blocks=1,               # limits on batch job requests
        max_blocks=1,              # max batch jobs
        parallelism=0.1,            # reduce "extra" batch jobs
        scheduler_options="#SBATCH -L SCRATCH,projecta \n#SBATCH --constraint=haswell",
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
        channel=LocalChannel(),    # batch communication is performed on this local machine
        launcher=SingleNodeLauncher()
    ),
)


## This executor is intended to be used for interactive work on a single login node
coriHlocal = HighThroughputExecutor(
    label='coriHlocal',
    address=address_by_hostname(),  # node upon which the top-level parsl script is running
    cores_per_worker=1,
    max_workers=1,                            # user tasks/node (small number to avoid hogging machine)
    poll_period=30,
    provider=LocalProvider(                 # Dispatch tasks on local machine only
        channel=LocalChannel(),
        init_blocks=1,
        max_blocks=1,
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
    )
)
## This executor is intended to be used for work on a single interactive batch node
coriHinteractive = HighThroughputExecutor(
    label='coriHinteractive',
    address=address_by_hostname(),  # node upon which the top-level parsl script is running
    cores_per_worker=1,
    max_workers=5,                            # user tasks/node (up to capacity of machine)
    poll_period=30,
    provider=LocalProvider(                 # Dispatch tasks on local machine only
        channel=LocalChannel(),
        init_blocks=1,
        max_blocks=1,
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
    )
)

## This is based on the *default* executor (*DO NOT USE* due to this
## executor is not recommended by Yadu)
coriLogin=ThreadPoolExecutor(
    label='coriLogin',
    managed=True,
    max_threads=2,
    storage_access=[],
    thread_name_prefix='',
    working_dir=None
)


###################################################
###################################################
###################################################

##
## Finally, assemble the full Parsl configuration 
##   [Be sure to specify your needed executor(s)]

config = Config(
    app_cache=True, 
    checkpoint_files=None, 
    checkpoint_mode='dfk_exit', 
    checkpoint_period=None, 
    executors=[
        coriBatchM
    ],
    monitoring=MonitoringHub(
        hub_address=address_by_hostname(),
        hub_port=55055,
        logging_level=logging.INFO,
        resource_monitoring_interval=60,
    ),
)



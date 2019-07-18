## pConfig.py - Define Parsl configuration for use in a top-level workflow script

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
from parsl.config     import  Config

## Parsl monitoring
from parsl.monitoring.monitoring import MonitoringHub
from parsl.addresses import address_by_hostname


##
##   Configure Parsl
##
hostName = address_by_hostname()


##
##  Define Parsl executors
##

## The following Executors are all based on the "High Throughput
## Executor" (or "HTEX") as recommended by the Parsl team.  They can
## operate on configuration ranging from a single login (or batch)
## node to many batch nodes.  These executors have been tuned for the
## makeBrighterFatterKernel.py DM tool.
#####################


## This executor is intended for large-scale KNL batch work with
## *multiple* nodes & workers/node and employing significant
## parallelism within the DM code ("-j")

knlMj = HighThroughputExecutor(
    label='knlMj',
    address=address_by_hostname(),   # node upon which the top-level parsl script is running
    cores_per_worker=25,             # threads per user task (managed by a 'worker')
    max_workers=2,                   # user tasks/node
    poll_period=30,
    provider=SlurmProvider(          ## Dispatch tasks via SLURM
        partition='regular',         # SLURM job "queue"
        walltime='05:00:00',         # max time for batch job
        cmd_timeout=90,              # Extend time waited in response to 'sbatch' command
        nodes_per_block=4,           # Nodes per batch job
        init_blocks=0,               # of batch jobs to submit in anticipation of future demand
        min_blocks=1,                # limits on batch job requests
        max_blocks=1, 
        parallelism=0.1,             # reduce "extra" batch jobs
        scheduler_options="#SBATCH -L SCRATCH,projecta \n#SBATCH --constraint=knl",
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
        channel=LocalChannel(),      # batch communication is performed on this local machine
        launcher=SrunLauncher()      # SrunLauncher necessary for multi-node batch jobs
    ),
)


## This executor is intended for large-scale KNL batch work with
## *multiple* nodes & workers/node but with minimal parallelism within
## the DM code itself.

knlM = HighThroughputExecutor(
    label='knlM',
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


## This executor is intended for batch work on a *single* KNL node
## with multiple workers

knl1 = HighThroughputExecutor(
    label='knl1',
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


## This executor is intended for batch work on a single Haswell node
## with multiple workers

haswell1 = HighThroughputExecutor(
    label='haswell1',
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


## This executor is intended to be used for interactive work on a
## single (haswell) login node

haswellint = HighThroughputExecutor(
    label='haswellint',
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


## This executor is intended to be used for work on a single
## interactive (haswell or knl) batch node

coriBint = HighThroughputExecutor(
    label='coriBint',
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
    checkpoint_mode='task_exit', 
    executors=[
        knlMj
    ],
    monitoring=MonitoringHub(
        hub_address=address_by_hostname(),
        hub_port=55055,
        logging_level=logging.INFO,
        resource_monitoring_interval=60,
    ),
    retries=2
)



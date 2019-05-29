## pConfig.py - python3 module to create a Parsl configuration for use in a top-level workflow script

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
from parsl.config       import  Config

## New Parsl monitoring (since v0.7.2)
from parsl.monitoring.monitoring import MonitoringHub
from parsl.addresses import address_by_hostname


##
##   Configure Parsl
##

## Old way of determining hostname
#if 'SLURMD_NODENAME' in os.environ:
#    hostName = os.environ['SLURMD_NODENAME']
#else:
#    hostName = os.environ['HOSTNAME']
#    pass
#print('Running on node determined by me:    ',hostName)

hostName = address_by_hostname()
print('Running on node determined by parsl: ',hostName)


##
##  Define some commonly used executors
##

## This executor is intended for large-scale batch work with multiple
## nodes and multiple workers/node
coriH = HighThroughputExecutor(
    label='coriH',
    address=address_by_hostname(),  # node upon which the top-level parsl script is running
    cores_per_worker=1,        # threads per user job
    max_workers=40,            # user tasks/node
    poll_period=30,
    provider=SlurmProvider(          # Dispatch tasks via SLURM
        partition='regular',               # SLURM job "queue"
        walltime='04:00:00',
        cmd_timeout=90,                # Extend time waited in response to 'sbatch' command
        nodes_per_block=1,      # Nodes per batch job
        init_blocks=0,                # of batch jobs to submit in anticipation of future demand
        min_blocks=1,               # limits on batch job requests
        max_blocks=5,
        parallelism=0.1,            # reduce "extra" batch jobs
        scheduler_options="#SBATCH -L SCRATCH,projecta \n#SBATCH --constraint=knl",
        worker_init=os.environ['PT_ENVSETUP'],          # Initial ENV setup
        channel=LocalChannel(),    # batch communication is performed on this local machine
        launcher=SingleNodeLauncher()
    ),
)


## This executor is intended to be used for interactive work on a single node
coriHlocal = HighThroughputExecutor(
    label='coriHlocal',
    address=address_by_hostname(),  # node upon which the top-level parsl script is running
    cores_per_worker=1,
    max_workers=1,                            # user tasks/node
    poll_period=30,
    provider=LocalProvider(                 # Dispatch tasks on local machine only
        channel=LocalChannel(),
        init_blocks=1,
        max_blocks=1,
        launcher=SimpleLauncher(),
        worker_init=os.environ['PT_ENVSETUP']          # Initial ENV setup
    )
)



##
## Finally, assemble the full Parsl configuration 
##

config = Config(
    app_cache=True, 
    checkpoint_files=None, 
    checkpoint_mode='dfk_exit', 
    checkpoint_period=None, 
    executors=[
        coriH,
        coriHlocal
    ],
    monitoring=MonitoringHub(
        hub_address=address_by_hostname(),
        hub_port=55055,
        logging_level=logging.INFO,
        resource_monitoring_interval=60,
    ),
)

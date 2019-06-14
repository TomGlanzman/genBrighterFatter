## BFworkflow.py - top-level Parsl workflow script to generate LSSTDESC brighter-fatter kernels

## T.Glanzman - April 2019

## Note: One must first have the proper python and DM environment to
## run this script.

##
## Initialization
##

import os,sys,datetime
import traceback

startTime = datetime.datetime.now()

## Say hello
print(startTime, ": Entering BFworkflow.py")
print("Running python from: ",sys.prefix)
print("Python version: ",sys.version)



#import logging

## Quantities used by all steps in this workflow
workflowRoot = os.environ['PT_WORKFLOWROOT']

## Load Parsl
import parsl
from parsl.app.app    import  python_app, bash_app
print("parsl version = ",parsl.__version__)

## Configure Parsl **USER-SUPPLIED configuration!**
import pConfig

print(datetime.datetime.now(), ": Parsl configuration setup complete")
print("config = ",pConfig.config)

parsl.load(pConfig.config)
print(datetime.datetime.now(), ": Parsl config complete!")

#########################################################
#########################################################


##
## Define Parsl-decorated workflow apps
##

@bash_app(executors=['coriBatchM'])
def genBF(cmd, stdout=parsl.AUTO_LOGNAME, stderr=parsl.AUTO_LOGNAME, label=None):
    ## Command executor - intended for BF kernel generation
    import os,sys,datetime
    print(datetime.datetime.now(),' Entering genBF')
    return f'{cmd}'

#########################################################
#########################################################

##
## Submit and Run the workflow steps
##

print(datetime.datetime.now(), ": Run BF generation")


## Define list of sensors for which to calculate BF kernel
#sensorList = [27]
#sensorList = [0,1,2,3,4,5,27,93,94,187]
sensorList = list(range(189))

## Submit parsl job steps ('tasks')
jobsk = []
jobsh = []
njobs = 0
for sensor in sensorList:
    njobs += 1
    cmd = workflowRoot+"/genBFkernel.sh "+str(sensor)+" "+str(sensor)+" "+os.environ['PT_RERUNDIR']+ " 1"
    print('cmd = ',cmd)
    stdo = os.path.join(workflowRoot,'Kernel'+str(njobs)+'.log')
    stde = os.path.join(workflowRoot,'KernelErr'+str(njobs)+'.log')
    print("Creating parsl task ",njobs-1)
    jobsk.append(genBF(cmd,label='makeBF'))
    pass
print(" Total number of parsl tasks created = ",njobs)

#########################################################
#########################################################

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
except Exception as ex:
    print("Exception waiting for job ",jobn)
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    print(traceback.format_exc())
    pass



## Final bookkeeping
endTime = datetime.datetime.now()
elapsedTime = endTime-startTime
print("Time to complete BF generation = ",elapsedTime)
print(endTime,": Exiting BFworkflow")

#sys.exit()





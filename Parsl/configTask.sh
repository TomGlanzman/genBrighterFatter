## configTask.sh 
##
## This file must be source'd by both the One-time Setup and
## Production Running steps
##
## Define environment variables to drive the generation of one set of
## brighter-fatter kernels on Cori at NERSC using SLURM and Parsl.
##
## Most variables defined herein will be prefixed with "PT_"
## ("ParslTask" or "PipelineTask", take your pick)
##


##################################################################################
###########  Global variables
##################################################################################

##     PT_WORKFLOWROOT is where the workflow scripts live
export PT_WORKFLOWROOT="$(dirname $(realpath $0))"
#echo "PT_WORKFLOWROOT = "$PT_WORKFLOWROOT

export PT_SCRATCH='/global/cscratch1/sd/descdm'

##     PT_OUTPUTDIR is the general area where the output goes, e.g., $SCRATCH or projecta
export PT_OUTPUTDIR=$PT_SCRATCH

##      PT_DEBUG is a global flag for workflow development & debugging
export PT_DEBUG=False

##################################################################################
###########  One-time Setup
##################################################################################

### The following values are required to establish a working DM-style
### repository

##### Define the inputs needed by BF kernel generation
export DESCDM_PREFIX=${PT_SCRATCH}'/DC2/Run2.1i'

## Location of the BF flats
export BF_FLAT_DATA_DIR=${DESCDM_PREFIX}/calibration/bf_flats_20190328_redo_test

##     PT_CALIBS points to a "CALIB" tar ball to populate the repository (is this needed??)
export PT_CALIBS='/global/projecta/projectdirs/lsst/production/DC2_ImSim/Run1.2i/CALIB/CALIB_Run1.2i.tar.gz'
##DEFUNCT##export CALIB_DIR=${DESCDM_PREFIX}/calib_repo


##     PT_REPODIR is the location of output repository
export PT_REPODIR=${PT_OUTPUTDIR}'/tomTest/bf_repoY'



##################################################################################
###########  Production running
##################################################################################

## makeBrighterFatterKernel parameters

##     PT_RERUNDIR is the subdirectory under <repo>/rerun into which results are stored
##                 Note that this value will be adjusted later with a numeric postfix.
export PT_RERUNDIR='Test6'

export PT_BF_DOCALCGAINS='False'

## Define the input BF-flat visit pairs
export PT_BF_VISITPAIRS="5000510,5000525 5000530,5000540 5000550,5000560 5000570,5000580 5000410,5000420 5000430,5000440 5000450,5000460 5000470,5000480 5000310,5000320 5000330,5000340 5000350,5000360 5000370,5000380 5000210,5000220 5000230,5000240 5000250,5000260 5000270,5000280 5000110,5000120 5000130,5000140 5000150,5000160 5000170,5000180"

#export PT_BF_OPTS=''


#----------------------------------------------------------------

## The following is used to define the Parsl "Config" object

### NOTE an intrinsic limitation of using env-vars to specify the
### Parsl "Config" data: with current naming scheme, this allows for
### only a *single* Config.  Multiple Configs are necessary if the
### shape of the task changes as Parsl works it way through the
### different processing steps.

##     PT_HOSTTYPE may be 'knl' or 'haswell'
export PT_HOSTTYPE='knl'

##     PT_ENVSETUP is a script run by the batch script prior to the main event
export PT_ENVSETUP="source ${PT_WORKFLOWROOT}/configTask.sh;export PATH="'${PATH}:${HOME}'"/.local/bin;source ${PT_WORKFLOWROOT}/cvmfsSetup.sh;"

##     PT_BATCHOPTS are any SLURM options needed by user code
##                  NOTE the peculiar way to include a NEWLINE character...
export PT_BATCHOPTS="#SBATCH -L SCRATCH,projecta "$'\n'"#SBATCH --constraint=${PT_HOSTTYPE}"

##     PT_WALLTIME time limit for SLURM jobs
export PT_WALLTIME='00:30:00'
#export PT_WALLTIME='02:00:00'

##     PT_QUEUE is the SLURM batch queue
export PT_QUEUE='debug'
#export PT_QUEUE='regular'

##     PT_JOBSPERNODE is the number of user job steps to run on a single Cori node
export PT_JOBSPERNODE=2

##     PT_CORESPERSTEP specifies single-threaded ("1") or multi-threaded (>1)
export PT_CORESPERSTEP=1

##     PT_NODESPERJOB is the number of Cori nodes to request per SLURM job
export PT_NODESPERJOB=1

##     PT_INITJOBS is the number of SLURM jobs to submit initially
export PT_INITJOBS=0

export PT_MINJOBS=1
export PT_MAXJOBS=1


## Dump all the "PT_" environent variables to screen
printenv |sort |grep "^PT_"

echo;echo;echo
echo "==========================================================================="
#echo "  ALL ENVIRONMENT VARIABLES "
## Dump all env-vars for debugging 
#printenv|sort
echo "==========================================================================="
echo;echo;echo

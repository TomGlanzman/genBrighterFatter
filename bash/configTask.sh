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

## Needed only until the most recent version of parsl is made part of the DM conda installation
export PATH="'${PATH}:${HOME}'"/.local/bin

####################################################################
###########  Global variables
####################################################################

##     PT_WORKFLOWROOT is where the workflow scripts live (does not work if this script is not sourced by another script)
export PT_WORKFLOWROOT="$(dirname $(realpath $0))"

export PT_SCRATCH='/global/cscratch1/sd/descdm'

##     PT_OUTPUTDIR is the general area where the output goes, e.g., $SCRATCH or projecta
export PT_OUTPUTDIR=$PT_SCRATCH

##      PT_DEBUG is a global flag for workflow development & debugging
export PT_DEBUG=False

####################################################################
###########  One-time Setup
####################################################################

### The following values are required to establish a working DM-style
### repository

##### Define the inputs needed by BF kernel generation
export PT_DESCDM_PREFIX=${PT_SCRATCH}'/DC2/Run2.1i'

## Location of the BF flats
#export BF_FLAT_DATA_DIR=${PT_DESCDM_PREFIX}/calibration/bf_flats_20190328_redo_test
export PT_BF_FLAT_DIR=${PT_DESCDM_PREFIX}/calibration/bf_flats_20190408/*

##     PT_CALIBS points to a "CALIB" tar ball to populate the repository (is this needed??)
export PT_CALIBS='/global/projecta/projectdirs/lsst/production/DC2_ImSim/Run1.2i/CALIB/CALIB_Run1.2i.tar.gz'

##     PT_REPODIR is the location of output repository
export PT_REPODIR=${PT_OUTPUTDIR}'/tomTest/bf_20190501'



####################################################################
###########  Production running
####################################################################

## makeBrighterFatterKernel parameters

##     PT_RERUNDIR is the subdirectory under <repo>/rerun into which results are stored
##                 Note that this value will be adjusted later with a numeric postfix.
export PT_RERUNDIR='20190501'


## Dump all the "PT_" environent variables to screen
printenv |sort |grep "^PT_"

echo;echo;echo
echo "==========================================================================="
#echo "  ALL ENVIRONMENT VARIABLES "
## Dump all env-vars for debugging 
#printenv|sort
echo "==========================================================================="
echo;echo;echo

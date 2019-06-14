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

## This script *must* be sourced to have any value!
if [[ x$BASH_SOURCE =~ x$0 ]]; then
    echo "You must source this script: $BASH_SOURCE"
    exit
fi

## Needed only until the most recent version of parsl is made part of the DM conda installation
export PATH="'${PATH}:${HOME}'"/.local/bin


#####################################################
###########  Global variables
#####################################################

##     PT_WORKFLOWROOT is where the workflow scripts live (must be same dir as this config script)
export PT_WORKFLOWROOT="$(realpath $(dirname $BASH_SOURCE))"
#echo "PT_WORKFLOWROOT = "$PT_WORKFLOWROOT

export PT_SCRATCH='/global/cscratch1/sd/descdm'

##     PT_OUTPUTDIR is the general area where the output goes, e.g., $SCRATCH or projecta
export PT_OUTPUTDIR=$PT_SCRATCH

##      PT_DEBUG is a global flag for workflow development & debugging
export PT_DEBUG=False

#####################################################
###########  One-time Setup
#####################################################

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
export PT_REPODIR=${PT_OUTPUTDIR}'/tomTest/bf_repoA'



###################################################
###########  Production running
###################################################

## makeBrighterFatterKernel parameters

##     PT_RERUNDIR is the subdirectory under <repo>/rerun into which results are stored
##                 Note that this value will be adjusted later with a numeric postfix.
export PT_RERUNDIR='20190611'

## Define the input BF-flat visit pairs
export PT_BF_VISITPAIRS="5000510,5000525 5000530,5000540 5000550,5000560 5000570,5000580 5000410,5000420 5000430,5000440 5000450,5000460 5000470,5000480 5000310,5000320 5000330,5000340 5000350,5000360 5000370,5000380 5000210,5000220 5000230,5000240 5000250,5000260 5000270,5000280 5000110,5000120 5000130,5000140 5000150,5000160 5000170,5000180"

#export PT_BF_OPTS=''

#----------------------------------------------------------------

## The following is used in association with the Parsl "Config" object

##     PT_ENVSETUP is a script run by the batch script prior to the main event
export PT_ENVSETUP="source ${PT_WORKFLOWROOT}/configTask.sh;export PATH="'${PATH}:${HOME}'"/.local/bin;source ${PT_WORKFLOWROOT}/cvmfsSetup.sh;"


## Dump all the "PT_" environent variables to screen
printenv |sort |grep "^PT_"

echo;echo;echo
echo "==========================================================================="
#echo "  ALL ENVIRONMENT VARIABLES "
## Dump all env-vars for debugging 
#printenv|sort
echo "==========================================================================="
echo;echo;echo

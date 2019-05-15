#!/bin/bash
## fullFP-1.sh - run a series of jobs to produce bfKernels for the entire LSST focal plane
##
## This script is optimized to run on a Cori-Haswell node


echo `date` " configTask.sh"
source configTask.sh

echo `date` " cvmfsSetup.sh"
source cvmfsSetup.sh

## Generate BF kernels

cd $PT_WORKFLOWROOT
/usr/bin/time -v ./genBFkernel.sh   0  31 "${PT_RERUNDIR}.1" 32 |tee block1.log
echo;echo;echo;echo;echo "++++++++++";echo;echo;echo;echo;echo
/usr/bin/time -v ./genBFkernel.sh  32  63 "${PT_RERUNDIR}.2" 32 |tee block2.log
echo;echo;echo;echo;echo "++++++++++";echo;echo;echo;echo;echo
/usr/bin/time -v ./genBFkernel.sh  64 95 "${PT_RERUNDIR}.3" 32 |tee block3.log

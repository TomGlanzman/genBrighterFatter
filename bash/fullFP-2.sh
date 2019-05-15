#!/bin/bash
## fullFP-2.sh - run a series of jobs to produce bfKernels for the entire LSST focal plane
##
## This script is optimized to run on a Cori-Haswell node


echo `date` " configTask.sh"
source configTask.sh

echo `date` " cvmfsSetup.sh"
source cvmfsSetup.sh

## Generate BF kernels

cd $PT_WORKFLOWROOT
/usr/bin/time -v ./genBFkernel.sh 96 127 "${PT_RERUNDIR}.4" 32 |tee block4.log
echo;echo;echo;echo;echo "++++++++++";echo;echo;echo;echo;echo
/usr/bin/time -v ./genBFkernel.sh 128 159 "${PT_RERUNDIR}.5" 32 |tee block5.log
echo;echo;echo;echo;echo "++++++++++";echo;echo;echo;echo;echo
/usr/bin/time -v ./genBFkernel.sh 160 188 "${PT_RERUNDIR}.6" 28 |tee block6.log

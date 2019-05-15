#!/bin/bash
## single.sh - run a single sensor B/F kernel
##
## This script is optimized to run on a Cori-Haswell node


echo `date` " configTask.sh"
source configTask.sh

echo `date` " cvmfsSetup.sh"
source cvmfsSetup.sh

## Generate BF kernels

cd $PT_WORKFLOWROOT
/usr/bin/time -v ./genBFkernel.sh   0  0 "${PT_RERUNDIR}.1" 1 |tee single1.log

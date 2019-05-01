#!/bin/bash
## fullFP.sh - run a series of jobs to produce bfKernels for the entire LSST focal plane
##
## This script is optimized to run on a Cori-Haswell node

cd $PT_WORKFLOWROOT
/usr/bin/time -v ./genBFkernel.sh   0  39 "${PT_RERUNDIR}.1" 40 |tee block1.log
/usr/bin/time -v ./genBFkernel.sh  40  79 "${PT_RERUNDIR}.2" 40 |tee block2.log
/usr/bin/time -v ./genBFkernel.sh  80 119 "${PT_RERUNDIR}.3" 40 |tee block3.log
/usr/bin/time -v ./genBFkernel.sh 120 159 "${PT_RERUNDIR}.4" 40 |tee block4.log
/usr/bin/time -v ./genBFkernel.sh 160 189 "${PT_RERUNDIR}.5" 40 |tee block5.log

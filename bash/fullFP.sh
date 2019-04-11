#!/bin/bash
## fullFP.sh - run a series of jobs to produce bfKernels for the entire LSST focal plane
##
## This script is optimized to run on a Cori-Haswell node

cd /global/u1/d/descdm/tomTest/DMtests2
/usr/bin/time -v ./genBFkernel.sh   0  39 block1 40 |tee block1.log
/usr/bin/time -v ./genBFkernel.sh  40  79 block2 40 |tee block2.log
/usr/bin/time -v ./genBFkernel.sh  80 119 block3 40 |tee block3.log
/usr/bin/time -v ./genBFkernel.sh 120 159 block4 40 |tee block4.log
/usr/bin/time -v ./genBFkernel.sh 160 189 block5 40 |tee block5.log

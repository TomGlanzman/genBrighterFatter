#!/bin/bash
## oneSensor.sh - generate a test BF kernel
##
## This script is optimized to run on a Cori-Haswell node

cd /global/u1/d/descdm/tomTest/DMtests2
/usr/bin/time -v ./genBFkernel.sh   0  1  block1 2 |tee block1.log


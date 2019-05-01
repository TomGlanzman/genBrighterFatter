#/bin/bash

## genBFkernel.sh - produce brighter-fatter kernels

## NOTE: a proper DM environment AND repository must first be
## established prior to running this script

if [ -z "$SLURMD_NODENAME" ]
then
    echo `date`"  Entering genBFkernel.sh, running on "${SLURMD_NODENAME}
else
    echo `date`"  Entering genBFkernel.sh, running on "${HOSTNAME}
fi


## command line args
startDet=$1       # beginning detector number (0-189)
endDet=$2         # last detector number
dir=$3            # name for /rerun subdirectory
nPar=$4           # number of parallel processes ('-j' option)

echo $0 $1 $2 $3 $4
echo "startDet "$1
echo "endDet  "$2
echo "dir          "$3
echo "nPar       "$4

PWDSAVE=$PWD

######################################
# Make BF correction kernel

## Timing prefix
Tprefix="/usr/bin/time -v "

## Optional makeBrighterFatterKernel.py parameters
BFoptions=" -j "${nPar}    ## parallelization

detectors=${startDet}".."${endDet}
visitPairs="5000510,5000525 5000530,5000540 5000550,5000560 5000570,5000580 5000410,5000420 5000430,5000440 5000450,5000460 5000470,5000480 5000310,5000320 5000330,5000340 5000350,5000360 5000370,5000380 5000210,5000220 5000230,5000240 5000250,5000260 5000270,5000280 5000100,5000110 5000120,5000130 5000140,5000150 5000160,5000170"
echo 'detectors = '$detectors
echo 'visitPairs = '$visitPairs

BFprefix=${CP_PIPE_DIR}/bin
echo "[makeBrighterFatterKernel.py]"
## set "doCalcGains=True" to compute bf gains from flats
## set "doCalcGains=False" to use bf gains stored in <repo>/calibrations

set -x
${Tprefix} python3 ${BFprefix}/makeBrighterFatterKernel.py "${PT_REPODIR}" --rerun ${dir}  --id detector=${detectors} --visit-pairs ${visitPairs} -c xcorrCheckRejectLevel=2 doCalcGains=False isr.doDark=True isr.doBias=True isr.doCrosstalk=True isr.doDefect=False isr.doLinearize=False forceZeroSum=True buildCorrelationModel=3 correlationQuadraticFit=True level=AMP --clobber-config --clobber-versions ${BFoptions}
rc=$?
set +x
echo "[rc = "$rc"]"


echo `date`"  Exiting genBFkernel.sh"
 

exit 

#/bin/bash

## genBFkernel.sh - produce brighter-fatter kernels

## NOTE: a proper DM environment AND repository must first be
## established prior to running this script

pid=$$
if [ ! -z "${SLURMD_NODENAME}" ]
then
    echo `date`"  $pid Entering genBFkernel.sh, running on "${SLURMD_NODENAME}
else
    echo `date`"  $pid Entering genBFkernel.sh, running on "${HOST}
fi


## command line args
startDet=$1       # beginning detector number (0-189)
endDet=$2         # last detector number
dir=$3            # name for /rerun subdirectory
nPar=$4           # number of parallel processes ('-j' option)

echo "$pid $0"

echo;echo;echo
echo "All environment variables:"
printenv |sort
echo "==========================="
echo "module list"
module list 2>&1
echo "==========================="
echo;echo;echo




PWDSAVE=$PWD

######################################
# Make BF correction kernel

## Timing prefix
Tprefix="/usr/bin/time -v "

## Parallelization makeBrighterFatterKernel.py parameters
if [ "$startDet" = "$endDet" ]; then
    BFoptions=""
    detectors=${startDet}
    echo "Single sensor [${detectors}], no parallelization"
else
    BFoptions=" -j "${nPar}    ## parallelization
    detectors=${startDet}".."${endDet}
    echo "Multiple sensors [${detectors}], parallelization set to ${nPar}"
fi


## Note that $CP_PIPE_DIR comes from the DM stack setup
BFprefix=${CP_PIPE_DIR}/bin
echo "$pid [makeBrighterFatterKernel.py]"
## set "doCalcGains=True" to compute bf gains from flats
## set "doCalcGains=False" to use bf gains stored in <repo>/calibrations


## This is the DM code to generate the brighter-fatter kernels
set -x

## Update 5/30/2019 change buildCorrelationModel to correlationModelRadius
#ORIGINAL#${Tprefix} python ${BFprefix}/makeBrighterFatterKernel.py "${PT_REPODIR}" --rerun ${dir}  --id detector=${detectors} --visit-pairs ${PT_BF_VISITPAIRS} -c xcorrCheckRejectLevel=2 doCalcGains=True isr.doDark=True isr.doBias=True isr.doCrosstalk=True isr.doDefect=False isr.doLinearize=False forceZeroSum=True correlationModelRadius=3 correlationQuadraticFit=True level=AMP --clobber-config --clobber-versions ${BFoptions}

## DEV! - Attempt to improve reliability by restricting files in the .....runinfo/<label>/config directory
${Tprefix} python ${BFprefix}/makeBrighterFatterKernel.py "${PT_REPODIR}" --rerun ${dir}  --id detector=${detectors} --visit-pairs ${PT_BF_VISITPAIRS} -c xcorrCheckRejectLevel=2 doCalcGains=True isr.doDark=True isr.doBias=True isr.doCrosstalk=True isr.doDefect=False isr.doLinearize=False forceZeroSum=True correlationModelRadius=3 correlationQuadraticFit=True level=AMP  --clobber-config ${BFoptions}


rc=$?
set +x
echo "$pid [rc = "$rc"]"


echo `date`"  $pid Exiting genBFkernel.sh"
 
## Exit with return code
exit $rc

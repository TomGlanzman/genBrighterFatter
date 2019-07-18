#/bin/bash

## genBFkernel.sh - produce brighter-fatter kernels

## NOTE: a proper DM environment AND repository must first be
## established prior to running this script

## NOTE: due to possible interference in the rerun/<label>/config
## directory by parallel jobs, a single "seeding run" is needed prior
## to any production runs.  This is done by omitting the "--id"
## parameter, and can be triggered by setting the first parameter of
## this script to "-1"

pid=$$
if [ ! -z "${SLURMD_NODENAME}" ]
then
    echo `date`"  $pid Entering genBFkernel.sh, running on "${SLURMD_NODENAME}
else
    echo `date`"  $pid Entering genBFkernel.sh, running on "${HOST}
fi


## command line args
startDet=$1       # beginning detector number (0-189), "-1" = seeding run
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

## The following might be necessary to prevent DM repo initialization contention
# delay=$(($RANDOM % 300))  ## 0-299 seconds
# echo "INITIAL RANDOM DELAY OF $delay SEC"
# sleep $delay
# echo `date`"  << Wake up! >>"

PWDSAVE=$PWD

######################################
# Make BF correction kernel

## Timing prefix
Tprefix="/usr/bin/time -v "

## Set Initialization and Parallelization parameters
clobberParm=""
if [ "$startDet" = "-1" ]; then
    BFoptions=""
    IDparm=""
    clobberParm=" --clobber-config --clobber-version "
    echo "Initialization run for seeding the config"
elif [ "$startDet" = "$endDet" ]; then
    BFoptions=""
    IDparm=" --id detector=${startDet} "
    echo "Single sensor [${startDet}], no parallelization"
else
    BFoptions=" -j "${nPar}    ## parallelization
    IDparm=" --id detector=${startDet}..${endDet} "
    echo "Multiple sensors [${startDet}..${endDet}], parallelization set to ${nPar}"
fi


## Note that $CP_PIPE_DIR comes from the DM stack setup
BFprefix=${CP_PIPE_DIR}/bin
echo "PID=${pid} [makeBrighterFatterKernel.py]"


## This is the DM code to generate the brighter-fatter kernels
## set "doCalcGains=True" to compute bf gains from flats
## set "doCalcGains=False" to use bf gains stored in <repo>/calibrations
set -x

## This is the command to generate the BF kernels
${Tprefix} python ${BFprefix}/makeBrighterFatterKernel.py "${PT_REPODIR}" --rerun ${dir}  ${IDparm} --visit-pairs ${PT_BF_VISITPAIRS} -c xcorrCheckRejectLevel=2 doCalcGains=True isr.doDark=True isr.doBias=True isr.doCrosstalk=True isr.doDefect=False isr.doLinearize=False forceZeroSum=True correlationModelRadius=3 correlationQuadraticFit=True level=AMP ${clobberParm} ${BFoptions}


rc=$?
set +x
echo "$pid [rc = "$rc"]"


echo `date`"  $pid Exiting genBFkernel.sh"
 
## Exit with return code
exit $rc

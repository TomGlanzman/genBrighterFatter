#!/bin/sh

## cvmfsSetup.sh - from Heather Kelly (3/21/2019) to set up DMstack
## envrironment within which to run the BF kernel generation code.
## Work in progress!
## Update: 4/30/2019 to use w_2019_17
## Update: 5/30/2019 to use w_2019_19 and new cp_pipe


export STACKCVMFS=/cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib
export LSST_STACK_VERSION=w_2019_19

export LOCALDIR=/global/common/software/lsst/cori-haswell-gcc/DC2/bf_kernel/software

module unload python
module unload python3

module swap PrgEnv-intel PrgEnv-gnu
module load pe_archive
module swap gcc gcc/6.3.0
module rm craype-network-aries
module rm cray-libsci
module unload craype
export CC=gcc

source $STACKCVMFS/$LSST_STACK_VERSION/loadLSST.bash
setup lsst_distrib
setup -r $LOCALDIR/cp_pipe-DM-18683-w_2019_19/cp_pipe -j
#setup -r $LOCALDIR/cp_pipe -j
#setup -r $LOCALDIR/obs_lsst -j

export OMP_NUM_THREADS=1


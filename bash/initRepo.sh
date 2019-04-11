#/bin/bash

## initRepo.sh - establish a DM-style repository in which to generate
## brighter-fatter kernels (and gains)

## NOTE: you must have a DM environment set up prior to running this
## script.


echo `date`"  Entering initRepo.sh"
 
##### Define the inputs needed by BF kernel generation
DESCDM_PREFIX=/global/cscratch1/sd/descdm/DC2/Run2.1i
BF_FLAT_DATA_DIR=${DESCDM_PREFIX}/calibration/bf_flats
CALIB_DIR=${DESCDM_PREFIX}/calib_repo


##### Define output repository
LSSTCAM_REPO_DIR=$SCRATCH/tomTest/bf_repo2
PWDSAVE=$PWD


##### Initialize output repo (but only once!)
if [ ! -d ${LSSTCAM_REPO_DIR} ]; then
    mkdir ${LSSTCAM_REPO_DIR}
    echo "lsst.obs.lsst.imsim.ImsimMapper" > ${LSSTCAM_REPO_DIR}/_mapper

    echo `date` " [ingestImages.py flats]"
    ingestImages.py "${LSSTCAM_REPO_DIR}" "${BF_FLAT_DATA_DIR}"/*k/lsst_a_*.fits --mode=link
    echo "[rc = "$?"]"


    echo `date` " [Setup CALIB]"
    # This assumes a copy of Heather's 'CALIB' tarball resides just upstream of $LSSTCAM_REPO_DIR
    cd ${LSSTCAM_REPO_DIR}
    tar -xvzf ${LSSTCAM_REPO_DIR}/../CALIB_Run1.2i.tar.gz
    cd CALIB
    python symlink_flats.py
    cd $PWDSAVE

    ## Copy in the (fake) birghter-fatter gains
    echo `date` " [Setup BF gains]"
    mkdir ${LSSTCAM_REPO_DIR}/calibrations
    cp -pr ${LSSTCAM_REPO_DIR}/../fake/bfGain*.pkl ${LSSTCAM_REPO_DIR}/calibrations

fi


echo `date`"  Exiting initRepo.sh"
 

exit 

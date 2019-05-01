#/bin/bash

## initRepo.sh - establish a DM-style repository in which to generate
## brighter-fatter kernels (and gains)

## NOTE: you must have a DM environment set up prior to running this
## script.


echo `date`"  Entering initRepo.sh"
 
PWDSAVE=$PWD


##### Initialize output repo (but only once!)
if [ ! -d ${PT_REPODIR} ]; then
    mkdir ${PT_REPODIR}
    echo "lsst.obs.lsst.imsim.ImsimMapper" > ${PT_REPODIR}/_mapper

    echo `date` " [ingestImages.py flats]"
    ingestImages.py "${PT_REPODIR}" "${PT_BF_FLAT_DIR}"/lsst_a_*.fits --mode=link
    echo "[rc = "$?"]"


    echo `date` " [Setup CALIB]"
    # This assumes a copy of Heather's 'CALIB' tarball resides just upstream of $PT_REPODIR
    cd ${PT_REPODIR}
    tar -xvzf ${PT_REPODIR}/../CALIB_Run1.2i.tar.gz
    cd CALIB
    python symlink_flats.py
    cd $PWDSAVE

    ## Copy in the (fake) brighter-fatter gains
    echo `date` " [Setup BF gains]"
    mkdir ${PT_REPODIR}/calibrations
    cp -pr ${PT_REPODIR}/../fake/bfGain*.pkl ${PT_REPODIR}/calibrations

else
    echo "%ALERT: the requested repo directory already exists.  No action taken"
    echo ${PT_REPODIR}
fi


echo `date`"  Exiting initRepo.sh"
 

exit 

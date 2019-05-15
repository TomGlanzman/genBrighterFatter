  Instructions for generating Brighter-Fatter kernels as of 5/2/2019
  ======================================

Generating the B/F kernels is taking >1 hour per sensor on
Cori-haswell.  The basic idea is to run the kernel generation in an
interactive Cori-haswell batch job.  But since the time limit for that
job class is 4 hours, and the work is split into several blocks to
avoid over consuming system memory, this means a 2-part process.

Log into cori as descdm, then follow this sequence

     === PART I ===

(coriNN)   $ gimehaswell           # alias to obtain a 4-hour interactive job on haswell
(nid000NN) $ cd ~/tomTest/genBrighterFatter/bash
(nid000NN) $ bash fullFP-1.sh

This should take about 3 hours to complete.  Output data are stored
here: $SCRATCH/tomTest/bf_20190501/rerun/blockN/calibration where "N" is 1-6

     === PART II ===

(coriNN)   $ gimehaswell           # alias to obtain a 4-hour interactive job on haswell
(nid000NN) $ cd ~/tomTest/genBrighterFatter/bash
(nid000NN) $ bash fullFP-2.sh

This should take another 3 hours to complete.

If any jobs should fail, the simplist recovery is to clean-up and
rerun the jobs.

$ cd ~/tomTest/genBrighterFatter/bash     # remove stale log files for failed jobs
$ rm blockN.log

$ cd $SCRATCH/tomTest/bf_20190501/rerun   # remove stale output areas for failed jobs
$ rm -rf blockN


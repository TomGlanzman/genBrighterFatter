#!/bin/bash

## Generate BF kernels

echo `date` " configTask.sh"
source configTask.sh

echo `date` " cvmfsSetup.sh"
source cvmfsSetup.sh

echo `date` " fullFP.sh"
source fullFP.sh

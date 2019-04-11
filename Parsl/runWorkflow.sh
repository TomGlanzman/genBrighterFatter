#!/bin/bash

## runWorkflow.sh - run the BFworkflow.sh script after setting up environment(s)

## This script is intended to be run interactively, ideally from the
## workflow main directory.


## Define root workflow directory
##   Note: this will assume this script resides in the top-level task directory
workflowroot=$(dirname $(realpath $0))
echo 'workflowroot= '$workflowroot

## This is needed if parsl (or some other package) is installed locally
export PATH=$HOME/.local/bin:$PATH

## Define the workflow-specific env-vars
echo "source configTask.sh"
source $workflowroot/configTask.sh

## DM setup
echo "source workflowroot/cvmfsSetup.sh"
source $workflowroot/cvmfsSetup.sh

## Run the workflow
echo "python workflowroot/BFworkflow.py"
python $workflowroot/BFworkflow.py

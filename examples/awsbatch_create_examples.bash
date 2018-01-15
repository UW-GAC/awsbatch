#!/bin/sh
# bash commands to create jebdefs, compute environments, and queues
JFILE="create_ce_tm_opt_100.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_tm_r4_500.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_queue_tm_opt_100.json"
echo "Creating queue $JFILE"
aws batch create-job-queue --cli-input-json file://../json_files/$JFILE

JFILE="create_queue_tm_r4_500.json"
echo "Creating queue $JFILE"
aws batch create-job-queue --cli-input-json file://../json_files/$JFILE

JFILE="create_jobdef_tm_nomount.json"
echo "Registering jobdef $JFILE"
aws batch register-job-definition --cli-input-json file://../json_files/$JFILE

JFILE="create_jobdef_tm_sync.json"
echo "Registering jobdef $JFILE"
aws batch register-job-definition --cli-input-json file://../json_files/$JFILE

#
# spot stuff
#
JFILE="create_ce_tm_spot_opt_100.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_tm_spot_r4_500.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_queue_tm_spot_opt_100.json"
echo "Creating queue $JFILE"
aws batch create-job-queue --cli-input-json file://../json_files/$JFILE

JFILE="create_queue_tm_spot_r4_500.json"
echo "Creating queue $JFILE"
aws batch create-job-queue --cli-input-json file://../json_files/$JFILE

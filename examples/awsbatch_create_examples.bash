#!/bin/sh
# bash commands to create jebdefs, compute environments, and queues
# od ce with tags
JFILE="create_ce_od_opt_grm.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_od_opt_single.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_od_r4_single.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_od_r4_grm.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

# test
JFILE="create_ce_test_burden.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

# spot ce with tags
JFILE="create_ce_spot_opt_skat.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_spot_opt_grm.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_spot_opt_ht_grm.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_spot_c4_ht_grm.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_spot_opt_single.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_spot_r4_single.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE

JFILE="create_ce_spot_r4_grm.json"
echo "Creating CE $JFILE"
aws batch create-compute-environment --cli-input-json file://../json_files/$JFILE


# od queue for r4 and opt
JFILE="create_queue_od_opt.json"
echo "Creating queue $JFILE"
aws batch create-job-queue --cli-input-json file://../json_files/$JFILE

JFILE="create_queue_od_r4.json"
echo "Creating queue $JFILE"
aws batch create-job-queue --cli-input-json file://../json_files/$JFILE

# spot queue for r4 and opt
JFILE="create_queue_spot_opt.json"
echo "Creating queue $JFILE"
aws batch create-job-queue --cli-input-json file://../json_files/$JFILE

JFILE="create_queue_spot_r4.json"
echo "Creating queue $JFILE"
aws batch create-job-queue --cli-input-json file://../json_files/$JFILE




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

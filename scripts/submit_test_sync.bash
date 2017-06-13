#!/bin/sh
#
# script to execute aws cli batch request
jobDef=topmed_sync
jobName=test_sync
jobQueue=Optimal_topmed
vcpus=1
mem=3000
#  it's a bit tricky to create a json variable especially for job's parameters
#  in bash that's more readable than just a very long line
params='{ "msg": "test of sync complete",'
params+=' "jids": "No job dependencies for this test" }'

aws batch submit-job --job-name $jobName \
                     --job-queue $jobQueue  \
                     --job-definition $jobDef \
                     --parameters "$params" \
                     --container-overrides "{ \"vcpus\": $vcpus, \"memory\": $mem }"

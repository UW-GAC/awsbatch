#!/bin/sh
#
# script to execute aws cli batch request
jobDef=topmed_general
jobName=test_run_rscript
jobQueue=Optimal_topmed
vcpus=1
mem=3000
mem=3000
#  it's a bit tricky to create a json variable especially for job's parameters
#  in bash that's more readable than just a very long line
params='{ "wd": "/projects/batch",'
params+=' "dr": "/projects", '
params+=' "rd": "/projects/batch/test.bash", '
params+=' "ra": "/projects/batch/Rsleep.txt --time 4 --taskid 2", '
params+=' "db": "1", '
params+=' "po": "0", '
params+=' "lf": "runrscript.log", '
params+=' "mt": "mount -t nfs4 -o vers=4.1 172.255.44.97:/ /projects" }'

aws batch submit-job --job-name $jobName \
                     --job-queue $jobQueue  \
                     --job-definition $jobDef \
                     --parameters "$params" \
                     --container-overrides "{ \"vcpus\": $vcpus, \"memory\": $mem }"

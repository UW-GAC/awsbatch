## **awsbatch project** ##

This project both scripts and JSON files used for managing and testing AWS batch service associated with the TOPMed pipeline.

####json_files folder ####
The folder *json_files* contains JSON files for specifying job definitions, compute environments, and job queues in AWS batch.  These files can be used with AWS command line interface (CLI) for batch to create the job definitions, compute environments and job queues.

For example, the following command illustrates creating (or registering) a job definition using AWS CLI and the json file

    aws batch register-job-definition --cli-input-json file:///<full path to json_files>/topmed_jobdef_general.json

(Note: the configuration of AWS cli specifies the credentials with the necessary permissions for executing the AWS batch command)

####scripts folder ####
The "*scripts"* folder contains both python and bash scripts for managing and testing the batch service associated with TOPMed pipeline. 

The python scripts execute AWS batch services using AWS bot3 to help manage batch services more efficiently than using AWS batch console.  For example, to delete all the runnable jobs in a queue using the batch console currently only supports deleting runnable jobs one at a time.  So if there are numerous jobs in the runnable state (or there states for that matter), it's very tedious and lengthy to delete these jobs via the console.  Using a python script, all jobs in a particular state can be deleted executing the script once.  For example,

    delete_runnable_jobs.py

deletes all runnable jobs in a queue specified within the script.  

The bash scripts execute batch services via AWS CLI to submit test jobs.  There are currently the following test jobs:

 1. *submit_test_sync.bash* - submits a job to test the sync job
 2. *submit_test_rscript.bash* - submits a job to test the running of an R script


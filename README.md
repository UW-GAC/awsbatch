## **awsbatch project** ##

This project contains files used for help in managing and testing AWS batch service associated with the TOPMed pipeline.

#### *json_files folder* ####
The folder *json_files* contains JSON files for specifying job definitions, compute environments, and job queues in AWS batch.  These files can be used with AWS command line interface (CLI) for batch to create the job definitions, compute environments and job queues.

For example, the following command illustrates creating (or registering) a job definition using AWS CLI and the json file

    aws batch register-job-definition --cli-input-json file:///<relative or full path to json_files>/create_jobdef_tm_nomount.json

(Note: the configuration of AWS cli specifies the credentials with the necessary permissions for executing the AWS batch command)

#### *examples folder*  ####
The "*examples"* folder contains a python script (*batch_boto3_manage_jobs.py*)to help manage batch jobs and bash script (*awsbatch_create_examples.bash*) showing the shell commands for creating compute environments, queues, and job definitions in AWS Batch.  

The python script requires *aws boto3* to be installed (e.g., *sudo pip install boto3 --upgrade*).  Using this script, jobs can be listed, cancelled, terminated, etc.  See the help (*python batch_boto3_manage_jobs.py -h") for details.

The bash script requires *aws cli* to be installed (e.g., *sudo pip install awscli --upgrade*).  The script illustrates the shell commands the execute (using the json files in the *json_files* folder) to do the following:
1. Create compute environments that specify a custom AMI.  The custom AMI includes the "preloaded" TOPMed docker images for analysis pipeline (e.g., *uwgac/r343-topmed:master* and *uwgac/r343-topmed:devel*) and pulls down new TOPMed docker images when booted.  The custom AMI also mounts (at boot time via */etc/fstab*) an EFS volume containing TOPMed project data.  The AMI includes 200GB of local storage (mostly to support the docker images and temporary files)
2. Register (or creates) job definitions for on-demand computing and spot computing
3. Create job queues supporting the various compute environments

#### *test folder*  ####
The *test* folder contains a python script (*test_arrayjob.py*) for testing the TOPMed docker images using job arrays.  The script submits a single job and an array job to AWS batch service in a manner similar to TOPMed's analysis pipeline.  It currently executes a very simple R script that just sleeps for 10 seconds (and the R script is located in the EFS volume)

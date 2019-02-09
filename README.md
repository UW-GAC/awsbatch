## **awsbatch project** ##

This project contains files and scripts to help in managing AWS batch definitions associated with the TOPMed pipeline.  In AWS batch there are following types of definitions:
1. jobs
2. queues
3. compute environments

Managing these definitions can be done the following ways:
1. AWS command line interface (CLI) can be used to create or delete these definitions by providing a json file that specifies the attributes of a definition.  
2. Using boto3 python scripts can also create (or delete) these batch definitions.
3. A web interface (i.e., the AWS batch console) can also be used to manage batch definitions.

(Note: In order to use either of the first two methods listed above, AWS command line  interface (CLI) must be installed on the local computer and configured with the  appropriate credentials (e.g., AWS key and AWS secret key) to identify the AWS account.)

Job definitions are associated with a docker file and specifies the docker command to run the docker image (or container) within batch.  For the TOPmed pipeline there are basically three job definitions (one for each docker image):
1. TM_master
2. TM_devel
3. TM_roybranch

Because a job definitions do not change very frequently (and can also be updated), the AWS CLI and a corresponding json file  (in the *json_files* folder) is used to define and update the job definitions.

Batch queues are associated with compute environments and tend to change frequently. The most convenient way to manage queue definitions is by the web interface.

Compute environments change very frequently.  To obtain costs for any analysis, a unique tag must be defined in the compute environment.  In order to change a tag in a compute environment, the compute environment must first be deleted and then re-created with a new tag.  The python script *create_ce.py* is used to create compute environments.  Deleting of compute environments is easier to do using the web interace.

#### *create_ce.py* ####
This script creates compute environments in AWS batch.  Using a combination of command line arguments and a compute environment configuration json file (*cecontext.json*), new compute environments can be fairly easy to create.  Execute the command with the *--help* argument to see more details.

Here's an example of creating an compute environment using on-demand (the *EC2* type) pricing in the UW account:

    create_ce.py -n caitlin_topmed_od -t "name=caitlin,mode=t3,analysis=caitlin_topmed_od" -i "m5.2xlarge,c5.4xlarge" -a uw --type EC2

#### *cecontext.json* ####
A json file providing context and default attributes associated with compute environment definitions. It is processed by the *create_ce.py* script.  Most attributes can be changed with command line arguments to the *create_ce.py* script.

#### *cecontext.py* ####
A python module for processing the json file and imported by the *create_ce.py* script.

#### *json_files folder* ####
The folder *json_files* contains JSON files for specifying job definitions, compute environments, and job queues in AWS batch.  These files can be used with AWS command line interface (CLI) for batch to create the job definitions, compute environments and job queues.

For example, the following command illustrates creating (or registering) a job definition using AWS CLI and the json file

    aws batch register-job-definition --cli-input-json file:///<relative or full path to json_files>/create_jobdef_tm_devel.json

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

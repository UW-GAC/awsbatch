import getpass
import time
import os

import boto3

user = getpass.getuser()
t = str(int(time.time()))
lfile = user + "_" + t
defParams ={
    "wd" : "/projects/topmed/analysts/batch",
    "dr" : "/projects",
    "rd" : "/usr/local/analysis_pipeline/runRscript.sh",
    "ra" : "",
    "lf" : "runrscript.log",
    "tmo": "60",
    "db" : "1",
    "po" : "0",
    "at" : "0",
    "nomnt": "1"
}
defQueue = "TM_Opt_100_queue"
defJobdef = "TM_nomount"
defVcpus = 1
defMemory =  2000
defRegion = "us-west-2"
defDependsOn = []
defEnv = [ {"name": "R_LIBS_USER", "value": "/projects/resources/gactools/R_packages/library"} ]
memkey = "-m"

# the class for the region us-west-2
batchC = boto3.client('batch',region_name=defRegion)

# emulate params passed into pipelien
cmd = "/usr/local/analysis_pipeline/runRscript.sh"
args = ["/projects/batch/Rsleep.txt", "--time 4", "--taskid 99"]
printOnly = False
opts = { memkey: 2000}
defParams['wd'] = "/projects/batch"
holdid = None

# from pipeline code (aws_batch)

# process the args/kwargs to go the driver (rc); the r script from args (index 0); and the r script's args (rest of args)
defParams['rd'] = cmd
if args is None:
    args = []
defParams['ra'] = " ".join(args)

# printonly
if printOnly:
    defParams['po'] = "1"

# get memory option
if opts is None:
    opts = {}
else:
    if memkey in opts:
        defMemory = opts[memkey]
# check for hold (depends on)
if holdid is not None and holdid != []:
    defDependsOn = holdid

# submit a single job (like null_model) that subsequent jobs depend on ...
defJobName = "singlejob_boto3"
array_range = None
jids = []
trackID = defJobName + "_" + str(int(time.time()*100))
log_prefix = trackID
print("Submitting single job " + defJobName )
subOut = batchC.submit_job(
   jobName = defJobName,
   jobQueue = defQueue,
   jobDefinition = defJobdef,
   parameters = defParams,
   dependsOn = defDependsOn,
   containerOverrides = {
      "vcpus": defVcpus,
      "memory": defMemory,
      "environment": defEnv
   }
)
# append jids
jids.append( { "jobId": subOut["jobId"] } )
print(">>> job id: " + str(jids))
# array job depending on single job
defDependsOn = jids
defJobName = "arrayjob_boto3"
array_range = "1-10"
trackID = defJobName + "_" + str(int(time.time()*100))
log_prefix = trackID
# process array_range
air = [ int(i) for i in array_range.split( '-' ) ]
taskList = range( air[0], air[1]+1 )
noJobs = len(taskList)
print("Submitting array job " + defJobName + " with " + str(noJobs))
print("\tdepends on jobid: " + str(jids))
defParams["at"] = "1"
defEnv.append( { "name": "FIRST_INDEX", "value": str(taskList[0]) } )
# submit
subOut = batchC.submit_job(
   jobName = defJobName + "_" + str(noJobs),
   jobQueue = defQueue,
   arrayProperties = { "size": noJobs },
   jobDefinition = defJobdef,
   parameters = defParams,
   dependsOn = defDependsOn,
   containerOverrides = {
      "vcpus": defVcpus,
      "memory": defMemory,
      "environment": defEnv
   }
)
# append jids
jids.append( { "jobId": subOut["jobId"] } )

print(jids)

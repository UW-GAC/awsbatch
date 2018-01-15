import sys
import getpass
import time
from   argparse import ArgumentParser
import os

import boto3

# create functions associated with dictionary of actions
def cancel(jid):
    if verbose:
        print("Canceling job " + jid)
    res = batchC.cancel_job(jobId=jid, reason="canceling job")
    if verbose:
        print("result: " + str(res))
def terminate(jid):
    if verbose:
        print("Deleting job " + jid)
    res = batchC.terminate_job(jobId=jid, reason='terminating job')
    if verbose:
        print("result: " + str(res))
def list(queue, maxr, state):
    if verbose:
        print("Getting jobs in state " + state)
    jd = batchC.list_jobs(jobQueue = queue, maxResults=maxr, jobStatus=state)
    jids = [ adict['jobId'] for adict in jd['jobSummaryList'] ]
    return jids
# dictionary of actions
actions = {'cancel': cancel, 'terminate': terminate, 'list': list}

jobStates = ["running", "pending", "runnable", "succeeded" , "failed"]

defQueue = "TM_Opt_100_queue"
defJobdef = "TM_nomount"
defRegion = "us-west-2"
defJobState = jobStates[0]
defAction = actions.keys()[0]
defMaxResults = 300


# command line parser
parser = ArgumentParser( description = "Example managing jobs on aws batch queues" )
parser.add_argument( "-v", "--verbose", help = "Show verbose messages [default: false]",
                     action = "store_true")
parser.add_argument( "-q", "--queue", default = defQueue,
                     help = "aws batch queue to manage [default: " + defQueue + "]" )
parser.add_argument( "-r", "--region", default = defRegion,
                     help = "aws region [default: " + defRegion + "]" )
parser.add_argument( "-j", "--jobdef", default = defJobdef,
                     help = "aws batch job definition [default: " + defJobdef + "]" )
parser.add_argument( "--jobstate", default = defJobState,
                     help = "aws batch job type or state [default: " + defJobState + "]" )
parser.add_argument( "-a", "--action", default = defAction,
                     help = "aws batch action or command [default: " + defAction + "]" )
parser.add_argument( "-m", "--maxresults", type = int, default = defMaxResults,
                     help = "Maximum results of aws batch action [default: " + str(defMaxResults) + "]" )


args = parser.parse_args()
# set result of arg parse_args
queue = args.queue
jobdef = args.jobdef
region = args.region
verbose = args.verbose
jobstate = args.jobstate
action = args.action
maxresults = args.maxresults

# check for valid state and action
if jobstate not in jobStates:
    print("Input job state " + jobstate + " is invalid (" + str(jobStates) + ")")
    sys.exit(2)
if action not in actions:
    print("Input action " + action + " is invalid (" + str(actions) + ")")
    sys.exit(2)

print("Action: " + action + " / queue: " + queue + " / state: " + jobstate)
# the class for the region
batchC = boto3.client('batch',region_name=region)

# get a dictionary of jobs  (only a max of 300 will be returned even
# if maxResults = 1000)
jids = actions['list'](queue, maxresults, jobstate)
if action != 'list':
    for jid in jids:
        actions[action](jid)
else:
    for jid in jids:
        print(jid)

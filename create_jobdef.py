#! /usr/bin/env python
import     time
import     csv
import     sys
import     os
from       argparse import ArgumentParser
from       datetime import datetime, timedelta
import     jobdef

try:
    import boto3
except ImportError:
    print (__file__ + ": python boto3 not supported.")
    sys.exit(1)

# init globals
version='1.0'
msgErrPrefix='>>> Error: '
msgInfoPrefix='>>> Info: '
debugPrefix='>>> Debug: '
logPrefix='>>> Log: '

def pInfo(msg):
    tmsg=time.asctime()
    print(msgInfoPrefix+tmsg+": "+msg)

def pError(msg):
    tmsg=time.asctime()
    print(msgErrPrefix+tmsg+": "+msg)

def pDebug(msg):
    if debug:
        tmsg=time.asctime()
        print(debugPrefix+tmsg+": "+msg)
def Summary(hdr):
    print(hdr)
    print( '\tVersion: ' + version)
    print( '\tAWS credentials profile: ' + profile)
    print( '\tDocker image name: ' + jbd["containerProperties"]["image"])
    print( '\tJob definition name: ' + name)
    print( '\tDebug: ' + str(debug))
    print( '\tTest: ' + str(test))
    tmsg=time.asctime()
    print( '\tTime: ' + tmsg)
# defaults
defName = 'TM_roybranch'
defDocker = 'uwgac/topmed-roybranch'
defProfile = 'uw'
defJobfile = 'jobdef.json'

# parse input
parser = ArgumentParser( description = "script to register a job definition" )
parser.add_argument( "name", nargs = 1,
                     help = "Name of the job definition to create [required]" )
parser.add_argument( "-d", "--dockerimage", default = defDocker,
                     help = "Name of the docker image is use [default: " + defDocker + "]" )
parser.add_argument( "-j", "--jbdfile", default = defJobfile,
                     help = "Job definition json file [default: " + defJobfile + "]" )
parser.add_argument( "-p", "--profile", default = defProfile,
                     help = "AWS credentials profile [default: " + defProfile + "]" )
parser.add_argument( "-T", "--test", action="store_true", default = False,
                     help = "Test without executing [default: False]" )
parser.add_argument( "-D", "--Debug", action="store_true", default = False,
                     help = "Turn on debug output [default: False]" )
parser.add_argument( "-S", "--summary", action="store_false", default = True,
                     help = "Print summary prior to executing [default: False]" )
parser.add_argument( "--version", action="store_true", default = False,
                     help = "Print version of " + __file__ )
args = parser.parse_args()
# set result of arg parse_args
if len(args.name) > 1:
    pError('More than 1 argument provided ' + str(args.name))
    sys.exit(2)
name = args.name[0]
dockerimage = args.dockerimage
jbdfile = args.jbdfile
profile = args.profile
debug = args.Debug
summary = args.summary
test = args.test

# create the ce account context object
jbd = jobdef.jobdef(jobdef_file = jbdfile, verbose = debug).GetJobdef()
# docker image
jbd["containerProperties"]["image"] = dockerimage
# summary
Summary("Summary of " + __file__)
try:
    session = boto3.Session(profile_name=profile)
    batch_client = session.client('batch')
except Exception as e:
    pError('boto3 session or client exception ' + str(e))
    sys.exit(2)
if not test:
    try:
        res = batch_client.register_job_definition( jobDefinitionName = name,
                                                    type = jbd["type"],
                                                    parameters = jbd["parameters"],
                                                    containerProperties = jbd["containerProperties"],
                                                    retryStrategy = jbd["retryStrategy"]
                                                   )
    except Exception as e:
        pError('create_compute_environment error: ' + str(e))
        sys.exit(2)

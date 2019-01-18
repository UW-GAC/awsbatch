#! /usr/bin/env python
import     time
import     csv
import     sys
import     os
from       argparse import ArgumentParser
from       datetime import datetime, timedelta
import     cecontext

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
    print( '\tAccount context file: ' + ctxfile)
    print( '\tAccount compute context: ' + accntctx)
    print( '\tCE name: ' + name)
    print( '\tCE type: MANAGED')
    print( '\tCE state: ' + state)
    print( '\tCE service: ' + ce_servicerole)
    print( '\tCE instance types: ' + str(instancetypes))
    print( '\tCE AMI id: ' + amiid)
    print( '\tCE resources: ' + str(ce_resources))
    print( '\tAWS credentials profile: ' + profile)
    print( '\tDebug: ' + str(debug))
    print( '\tTest: ' + str(test))
    tmsg=time.asctime()
    print( '\tTime: ' + tmsg)
# defaults
defAccntCtx = 'uw'
defCtxfile = 'cecontext.json'

# parse input
parser = ArgumentParser( description = "script to a batch compute environment" )
parser.add_argument( "-n", "--name",
                     help = "Name of the compute environment to create [required]" )
parser.add_argument( "-C", "--ctxfile", default = defCtxfile,
                     help = "Compute environment context json file [default: " + defCtxfile + "]" )
parser.add_argument( "-a", "--accntctx", default = defAccntCtx,
                     help = "Account context [default: " + defAccntCtx + "]" )
parser.add_argument( "-t", "--tags",
                     help = "Tags as comma separated key, value pairs [default: 'Name=<ce name>']" )
parser.add_argument( "-i", "--instancetypes",
                     help = "Instance types as comma separated key, value pairs [default: value in ctx file]" )
parser.add_argument( "--amiid",
                     help = "AMI id [default: value in ctx file]" )
parser.add_argument( "--type",
                     help = "Compute environment resources type (SPOT or EC2) [default: value in ctx file]" )
parser.add_argument( "--state",
                     help = "Compute environment state (ENABLED or DISABLED) [default: value in ctx file]" )
parser.add_argument( "-p", "--profile",
                     help = "AWS credentials profile [default: based on accntctx]" )
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
name = args.name
ctxfile = args.ctxfile
accntctx = args.accntctx
tags = args.tags
debug = args.Debug
summary = args.summary
test = args.test
type = args.type
state = args.state
profile = args.profile
instancetypes = args.instancetypes
amiid = args.amiid

if name == None:
    pError("--name option is required.")
    sys.exit(2)

# create the ce account context object
cectx = cecontext.cecontext(ctx_file = ctxfile, verbose = debug)

if profile == None:
    profile = cectx.accntprofile(accntctx)
    if profile == None:
        pError("Profile not found based on account ctx " + accntctx)
        sys.exit(2)

if state == None:
    state = cectx.cstate()

# get all the ce resources based on accnt ctxt
ce_resources = cectx.allceresources(accntctx)
if ce_resources == None:
    pError("Invalid account context " + accntctx + " [" + str(cectx.accntnames()) + "]")
    sys.exit(2)
# instance types
if instancetypes == None:
    instancetypes = ce_resources['instanceTypes']
else:
    instancetypes = instancetypes.replace(' ','').split(',')
    ce_resources['instanceTypes'] = instancetypes
# ami id
if amiid == None:
    amiid = ce_resources['imageId']
else:
    ce_resources['imageId'] = amiid
# get the resource type
if type != None:
    ce_resources['type'] = type

# get the service role
ce_servicerole = cectx.accntservice(accntctx)
if ce_servicerole == None:
    pError("Cannot find the serviceRole for " + accntctx)
    sys.exit(2)
# add tags
if tags != None:
    tags = tags.replace('=',',')
    tags = tags.split(',')
    tl = [tag.strip() for tag in tags]
    tagdict = dict(zip(tl[::2],tl[1::2]))
    ce_resources['tags'] = tagdict

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
        res = batch_client.create_compute_environment(
                    computeEnvironmentName = name,
                    type = cectx.ctype(),
                    state = state,
                    computeResources = ce_resources,
                    serviceRole = ce_servicerole)
    except Exception as e:
        pError('create_compute_environment error: ' + str(e))
        sys.exit(2)

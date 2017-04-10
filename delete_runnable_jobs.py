#!/usr/local/bin/python
import getpass
import time
import os

import boto3
defQueue = "LowPriority"
defJobdef = "topmed_general"
defRegion = "us-east-1"

# the class for the region us-east-1
batchC = boto3.client('batch',region_name=defRegion)

# get a dictionar of runnable the jobs (only a max of 300 will be returned even
# if maxResults = 1000
jd = batchC.list_jobs(jobQueue = "LowPriority", maxResults=300, jobStatus="RUNNABLE")

# 3 keys to dict; we need jd['jobSummaryList'] which is a list of of dicts
# for all runnable jobs {'jobName': xx, 'jobId': yy}
jids = [ adict['jobId'] for adict in jd['jobSummaryList']]

# now delete them
for jid in jids:
    res = batchC.terminate_job ( jobId=jid,
                                reason='terminating jobs')

#This script submits jobs to the sunnyvale cluster (and resubmits jobs that stopped because of the 48hour walltime limit).

import os
import os.path
import glob
import numpy as np

def submit_job(f, job_name):
    os.system('mv %s %s'%(f, job_name))
    os.system('qsub %s'%job_name)
    os.system('mv %s %s'%(job_name,f))

jobs_dir = 'jobs/'

files = glob.glob('%s/*'%jobs_dir)
Njobs_counter = 0
for f in files:
    job_name = f.split(jobs_dir)[1]
    submit_job(f, job_name)     #submitting job for the first time
    Njobs_counter += 1

print 'submitted %d jobs'%Njobs_counter

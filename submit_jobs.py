#This script submits jobs to the sunnyvale cluster (and resubmits jobs that stopped because of the 48hour walltime limit).

import os
import os.path
import glob
import numpy as np

def submit_job(f, job_name):
    os.system('mv %s %s'%(f, job_name))
    os.system('qsub %s'%job_name)
    os.system('mv %s %s'%(job_name,f))

def find_unsubmitted_jobs(jobs_dir):
    unsub_jobs = []
    N_jobs_submitted = 0
    jobs = glob.glob('%s/*'%jobs_dir)
    for j in jobs:
        basename = os.path.basename(j)
        if os.path.isfile('output/%s_SA.bin'%basename) == False:
            unsub_jobs.append(j)
        else:
            N_jobs_submitted += 1
    print('N_jobs_submitted=%d'%N_jobs_submitted)
    print('found %d jobs'%len(unsub_jobs))
    return unsub_jobs

###############################

jobs_dir = 'jobs/jobs3/'                    #once jobs1 are finished, submit jobs2/ and then jobs3/

#files = glob.glob('%s/*'%jobs_dir)
files = find_unsubmitted_jobs(jobs_dir)     #find unsubmitted jobs

#Njobs_counter = 0
#for f in files:
#    job_name = f.split(jobs_dir)[1]
#    submit_job(f, job_name)     #submitting job for the first time
#    Njobs_counter += 1
#
#print('submitted %d jobs'%Njobs_counter)

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
    N_true = 0
    jobs = glob.glob('%s/*'%jobs_dir)
    for j in jobs:
        basename = os.path.basename(j)
        if os.path.isfile('output/%s_SA.bin'%basename) == False:
            unsub_jobs.append(j)
        elif os.path.isfile('output/%s_SA.bin'%basename) == True:
            N_true += 1
    print('N_true=%d'%N_true)
    return unsub_jobs

###############################

jobs_dir = 'jobs/jobs3/'                    #once jobs1 are finished, submit jobs2/ and then jobs3/

#files = glob.glob('%s/*'%jobs_dir)
files = find_unsubmitted_jobs(jobs_dir)     #find unsubmitted jobs

print("found %d jobs"%len(files))


#Njobs_counter = 0
#for f in files:
#    job_name = f.split(jobs_dir)[1]
#    submit_job(f, job_name)     #submitting job for the first time
#    Njobs_counter += 1
#
#print('submitted %d jobs'%Njobs_counter)

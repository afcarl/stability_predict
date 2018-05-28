#This script submits jobs to the sunnyvale cluster (and resubmits jobs that stopped because of the 48hour walltime limit).

import os
import os.path
import glob
import numpy as np

def submit_job(path, job_name):
    os.system('mv %s %s'%(path, job_name))
    os.system('qsub %s'%job_name)
    os.system('mv %s %s'%(job_name,path))

def find_unsubmitted_jobs(jobs_dir):
    unsub_jobs = []
    N_jobs_submitted = 0
    jobs = glob.glob('%s/*'%jobs_dir)
    for j in jobs:
        basename = os.path.basename(j)
        if os.path.isfile('output/%s_inc_SA_final.bin'%basename) == False:
            unsub_jobs.append(j)
        else:
            N_jobs_submitted += 1
    print('N_jobs_submitted=%d'%N_jobs_submitted)
    print('found %d jobs'%len(unsub_jobs))
    return unsub_jobs

def check_if_interrupted_job(job_output):
    file = open(job_output, 'r').read()
    if "finished simulation" in file:
        return False
    else:
        return True

###############################

system = "KOI-0085"
jobrange = [0,1000]        #[first, last] job to be submitted
shadow = 1

#files = find_unsubmitted_jobs(jobs_dir)     #find unsubmitted jobs and submit them

Njobs_counter = 0

# fixing interrupted jobs of KOI-0085
for i in np.arange(jobrange[0],jobrange[1]):
    job_name = '%s_1.0e+09orbits_id%d_shadow%d'%(system,i,shadow)
    job_output = 'job_output/%s'%job_name
    interrupted = check_if_interrupted_job(job_output)
    if interrupted:
        print(job_name)
        path = 'jobs/%s_final/%s'%(system,job_name)
        submit_job(path, job_name)     #submitting job for the first time
        Njobs_counter += 1

#for i in np.arange(jobrange[0],jobrange[1]):
#    job_name = '%s_1.0e+09orbits_id%d_shadow%d'%(system,i,shadow)
#    path = 'jobs/%s_final/%s'%(system,job_name)
#    submit_job(path, job_name)     #submitting job for the first time
#    Njobs_counter += 1

print('submitted %d jobs over jobrange %d-%d'%(Njobs_counter,jobrange[0],jobrange[1]))

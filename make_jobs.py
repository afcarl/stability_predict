#The purpose of this script is to generate the jobs that will be simulated by run_Nbody.py, and submitted to sunnyvale through submit_jobs.py
import numpy as np
import pandas as pd
import sys
import os

#star mass for each system
Ms = {};
Ms["KOI-0156"] = 0.56; Ms["KOI-0168"] = 1.11; Ms["KOI-2086"] = 1.04; Ms["Kepler-431"] = 1.071;
Ms["KOI-0085"] = 1.25; Ms["KOI-0115"] = 0.961; Ms["KOI-0152"] = 1.165; Ms["KOI-0250"] = 0.544;
Ms["KOI-0314"] = 0.521; Ms["KOI-0523"] = 1.07; Ms["KOI-0738"] = 0.979; Ms["KOI-1270"] = 0.83;
Ms["KOI-1576"] = 0.907;

#epoch
epoch = 780

####################################################
def generate_jobs(system,dir,n_sims,norbits,id_offset):
    orb_elements = ["m1","T1","P1","h1","k1","m2","T2","P2","h2","k2","m3","T3","P3","h3","k3"]
    
    N_columns = len(pd.read_csv("systems/data_files/%s.dat"%system,sep="\s+").columns)
    if N_columns < 15:
        print("**The number of planets in the system is %f, *not* generating jobs**"%N_columns/5.)
        return 0
    elif N_columns > 15:
        print("The number of planets in the system is %f, generating jobs"%N_columns/5.)
        orb_elements = []
        for i in range(N_columns/5):
            orb_elements.append(["m%d"%i,"T%d"%i,"P%d"%i,"h%d"%i,"k%d"%i])
    Np = int(N_columns/5)

    datafull = pd.read_csv("systems/data_files/%s.dat"%system,names=orb_elements,sep="\s+")

    #get random samples from full posterior
    rN = np.random.randint(0,len(datafull),n_sims)
    data = datafull.iloc[rN].reset_index(drop=True)
    data.index += id_offset
    data.to_csv("systems/%s_data.csv"%system, mode="a", header=np.logical_not(os.path.isfile("systems/%s_data.csv"%system)))

    #generate jobs
    for shadow in [0,1]:
        for sample in data.iterrows():
            id_ = sample[0]             #id number of sample
            job_name = "%s_1e%dorbits_id%d_shadow%d"%(system,int(np.log10(norbits)),id_,shadow)
            sh_script_name = "%s%s"%(dir,job_name)
            with open(sh_script_name, 'w') as f:
                f_head = open('job_header_sunnyvale','r')
                f.write(f_head.read())
                f_head.close()
                f.write('#PBS -N %s \n'%job_name)
                f.write('# EVERYTHING ABOVE THIS COMMENT IS NECESSARY, SHOULD ONLY CHANGE nodes,ppn,walltime and my_job_name VALUES\n')
                f.write('cd $PBS_O_WORKDIR\n')      #This will be the home stability_predict directory
                f.write('source /mnt/raid-cita/dtamayo/stability/bin/activate \n')
                f.write('python run_Nbody.py %s %d %f %.2f %d %d %d %s >& batch.output\n'%(system,id_,Ms[system],epoch,norbits,Np,shadow,job_name))
            f.close()
    return 1

####################################################
if __name__ == '__main__':
    systems = ["KOI-1576"]
    
    dir = 'jobs/'           #output directory for jobs
    n_sims = 5            #number of sims created (x2 for shadow systems)
    norbits = 1e9           #number of orbits of innermost planet
    id_offset = 5           #id offset number so that you dont overwrite previous job names.
    
    for system in systems:
        out = generate_jobs(system,dir,n_sims,norbits,id_offset)



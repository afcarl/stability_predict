#The purpose of this script is to generate the jobs that will be simulated by run_Nbody.py, and submitted to sunnyvale through submit_jobs.py
import numpy as np
import pandas as pd
import sys
import os
import forecaster.mr_forecast as mr
from random import random, uniform, seed
import systems.sys_params as sysp

# get planetary systems
nomass_sys, vaneye_sys, danjh_sys = sysp.get_system_lists()

# get star mass/uncertainties for each system
Ms = sysp.get_Ms()

#epoch
epoch = 780

########### Gaussian sampler, including systems with asymmetric error bars ###########
def draw_from_gaussian(tuple, n_samples):
    mean, upper, lower = tuple
    if upper == lower:
        return np.random.normal(mean, upper, n_samples)
    else:
        up_samp, low_samp = [], []
        while len(up_samp) < n_samples/2 and len(low_samp) < n_samples/2:
            up_samp = np.random.normal(mean, upper, 2*n_samples)
            up_samp = up_samp[up_samp > mean]
            low_samp = np.random.normal(mean, lower, 2*n_samples)
            low_samp = low_samp[low_samp <= mean]
        samples = np.concatenate((up_samp[0:n_samples/2], low_samp[0:n_samples/2]))
        np.random.shuffle(samples)
        return samples

########### Helper function for systems with no masses ###########
def draw_e(Ms, P1, P2, P3, m1, m2, m3):
    a1, a2, a3 = ((P1/365)**2 * Ms)**(1./3.), ((P2/365)**2 * Ms)**(1./3.), ((P3/365)**2 * Ms)**(1./3.)
    
    ecrit1 = (a2-a1)/a1
    ecrit21 = (a2-a1)/a2
    ecrit23 = (a3-a2)/a2
    ecrit3 = (a3-a2)/a3
    
    logemax1 = np.log10(ecrit1)
    logemax2 = np.log10(min(ecrit21, ecrit23))
    logemax3 = np.log10(ecrit3)
    
    earth = 0.000003003
    logemin1 = np.log10(m2*earth/ecrit1**2)
    logemin2 = np.log10(max(m1*earth/ecrit21**2, m3*earth/ecrit23**2))
    logemin3 = np.log10(m2*earth/ecrit3**2)
    
    e1 = min(10.**uniform(logemin1, logemax1), 1.) # make sure ecc < 1
    e2 = min(10.**uniform(logemin2, logemax2), 1.)
    e3 = min(10.**uniform(logemin3, logemax3), 1.)
    return e1, e2, e3

########### Main Routine ###########
def generate_jobs(system, dat_dir, jobs_dir, n_sims, norbits):
    
    if n_sims % 2 == 1:
        raise Exception("n_sims must be even for sampling purposes")
        return 0
    
    # randomly sample stellar mass
    star_mass = draw_from_gaussian(Ms[system], n_sims)
    
    # no masses/samples provided, generate probabilistically from mr_forecaster
    if system in nomass_sys:
        orb_params = ["m1","MA1","P1","e1","w1","m2","MA2","P2",
                      "e2","w2","m3","MA3","P3","e3","w3","Ms"]
        Np = 3
        rad, period = sysp.get_rad_and_period()
        
        # get probabilistic masses
        r1 = draw_from_gaussian(rad[system][0], n_sims)
        r2 = draw_from_gaussian(rad[system][1], n_sims)
        r3 = draw_from_gaussian(rad[system][2], n_sims)
        m1 = mr.Rpost2M(r1, unit='Earth', grid_size=1e3, classify='Yes')  #earth masses
        m2 = mr.Rpost2M(r2, unit='Earth', grid_size=1e3, classify='Yes')
        m3 = mr.Rpost2M(r3, unit='Earth', grid_size=1e3, classify='Yes')
        
        # randomly generate rest of orbital parameters
        P1, P2, P3 = period[system][0], period[system][1], period[system][2]
        w1, MA1 = 2*np.pi*np.random.random(n_sims), 2*np.pi*np.random.random(n_sims)
        w2, MA2 = 2*np.pi*np.random.random(n_sims), 2*np.pi*np.random.random(n_sims)
        w3, MA3 = 2*np.pi*np.random.random(n_sims), 2*np.pi*np.random.random(n_sims)
        e1 = np.random.beta(a=0.867, b=3.03, size=n_sims)   # Kipping (2013)
        e2 = np.random.beta(a=0.867, b=3.03, size=n_sims)
        e3 = np.random.beta(a=0.867, b=3.03, size=n_sims)
#        e = []
#        for i in range(n_sims):
#            e.append(draw_e(star_mass[i], P1, P2, P3, m1[i], m2[i], m3[i]))
#        e1, e2, e3 = list(zip(*np.asarray(e)))

        # store in data frame
        data = []
        for i in range(n_sims):
            data.append([m1[i], MA1[i], P1, e1[i], w1[i], m2[i], MA2[i], P2, e2[i],
                         w2[i], m3[i], MA3[i], P3, e3[i], w3[i], star_mass[i]])
        data = pd.DataFrame(np.asarray(data), columns=orb_params)
    else:
        # van-eyelen samples
        if system in vaneye_sys:
            orb_params = ["T1","b1","e1","w1","r1/rs","Fs1","T2","b2","e2","w2","r2/rs",
                          "Fs2","T3","b3","w3","e3","r3/rs","Fs3","gam1","gam2"]
            samples = np.load("systems/data_files/van_eylen/%s/chain_period_eccentricity_finalone.dat.npy"%system)
            s = samples.shape
            datafull = pd.DataFrame(samples.reshape(s[0]*s[1],s[2]), columns=orb_params)

        # daniel jontoff-hutter samples
        elif system in danjh_sys:
            # check that it's a 3-planet system
            N_columns = len(pd.read_csv("systems/data_files/jontoff-hutter/%s.dat"%system,sep="\s+").columns)
            Np = int(N_columns/5)
            if N_columns < 15:
                print("**The number of planets in system %s is %f, *not* generating jobs**"%(system,N_columns/5.))
                return 0
            elif N_columns > 15:
                print("The number of planets in system %s is %f, generating jobs"%(system,N_columns/5.))
                orb_params = ["m1","T1","P1","h1","k1","m2","T2","P2",
                              "h2","k2","m3","T3","P3","h3","k3"]
            # load full posterior
            datafull = pd.read_csv("systems/data_files/%s.dat"%system, names=orb_params, sep="\s+")
        else:
            print("system not found")
            return 0
        # get random samples from full posterior, store in data frame
        rN = np.random.randint(0, len(datafull), n_sims)
        data = datafull.iloc[rN].reset_index(drop=True)
        data["Ms"] = star_mass

    #*****make a function later that double checks that each new drawn sample isn't a copy of a previous one?

    # Save data to csv
    incl_header=True
    data_file = "%s/%s_data.csv"%(dat_dir, system)
    # if file already exists, start current index number at previous entry number
    if os.path.isfile(data_file) == True:
        data.index += pd.read_csv(data_file).index[-1] + 1
        incl_header=False
    data.to_csv(data_file, mode="a", header=incl_header)

    # Generate jobs
    cluster_type = 'aci-b'      #sunnyvale or aci-b
    shadow = 0
#    for shadow in [0,1]:
    for sample in data.iterrows():
        id_ = sample[0]             #id number of sample
        job_name = "%s_1e%dorbits_id%d_shadow%d"%(system,int(np.log10(norbits)),id_,shadow)
        sh_script_name = "%s%s"%(jobs_dir, job_name)
        if cluster_type == 'sunnyvale':
            with open(sh_script_name, 'w') as f:
                f_head = open('job_header_sunnyvale','r')
                f.write(f_head.read())
                f_head.close()
                f.write('#PBS -N %s \n'%job_name)
                f.write('# EVERYTHING ABOVE THIS COMMENT IS NECESSARY, SHOULD ONLY CHANGE nodes,ppn,walltime and my_job_name VALUES\n')
                f.write('cd $PBS_O_WORKDIR\n')      #This will be the home stability_predict directory
                f.write('source /mnt/raid-cita/dtamayo/stability/bin/activate \n')
                f.write('python run_Nbody.py %s %d %.2f %d %d %d %s >& batch.output\n'%(system,id_,epoch,norbits,Np,shadow,job_name))
                f.close()
        elif cluster_type == 'aci-b':
            with open(sh_script_name, 'w') as f:
                f_head = open('job_header_aci-b','r')
                f.write(f_head.read())
                f_head.close()
                f.write('python run_Nbody.py %s %d %.2f %d %d %d %s >& batch.output\n'%(system,id_,epoch,norbits,Np,shadow,job_name))
                f.close()
    return 1

####################################################
if __name__ == '__main__':
    #systems = ["KOI-0085","KOI-0115","KOI-0152","KOI-0156","KOI-0250","KOI-0314","KOI-0523","KOI-0738","KOI-1270","KOI-1576","KOI-2086","Kepler-446"]
    systems = ["EPIC-210897587-1","EPIC-210897587-2"]
    
    jobs_dir = "jobs/"     #output directory for jobs
    dat_dir = "systems"    #output directory for storing _data.csv files
    n_sims = 1000            #number of sims created (x2 for shadow systems!!)
    #norbits = 1e9           #number of orbits of innermost planet
    norbits = 5.8e9         #"EPIC-210897587-1/2 - 100 Myr"
    
    for system in systems:
        out = generate_jobs(system,dat_dir,jobs_dir,n_sims,norbits)
        print("Generated %d simulations for %s"%(n_sims,system))



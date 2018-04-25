# This function is needed to generate the required features from simulations so that predictions
# can be generated.

import pandas as pd
import numpy as np
import os
import rebound
import time
from collections import OrderedDict
import run_Nbody_inc as Nbod
import xgboost as xgb

#Certain parameters (e.g. inclination) might be 0, and so certain features might return NaN
def check_nan(x):
    if np.isnan(x):
        return 0
    else:
        return x

def get_M(e, w, T, P, epoch):
    f = np.pi/2 - w
    E = 2*np.arctan(np.tan(f/2) * np.sqrt((1-e)/(1+e))) #E and f always in same half of ellipse
    M = E - e*np.sin(E)
    return M + (epoch - T)*2*np.pi/P

# sim is generated from Nbod and passed here.
def generate_features(sim, iteration, maxorbs=10000, Nout=100, window=10):
    t0 = time.time()
    ps = sim.particles
    
    P0 = ps[1].P
    tmax = maxorbs * P0 # number of inner planet orbital periods to integrate
    
    sim.collision_resolve = Nbod.collision
    
    #kicksize=1.e-11
    #sim2.particles[2].x += kicksize
    
    E0 = sim.calculate_energy()
    times = np.linspace(0,tmax,Nout)
    
    a = np.zeros((sim.N,Nout))
    e = np.zeros((sim.N,Nout))
    inc = np.zeros((sim.N,Nout))
    
    beta12 = np.zeros( Nout)
    beta23 = np.zeros(Nout)
    
    Rhill12 = ps[1].a*((ps[1].m+ps[2].m)/3.)**(1./3.)
    Rhill23 = ps[2].a*((ps[2].m+ps[3].m)/3.)**(1./3.)
    
    eHill = [0, Rhill12/ps[1].a, max(Rhill12, Rhill23)/ps[2].a, Rhill23/ps[3].a]
    daOvera = [0, (ps[2].a-ps[1].a)/ps[1].a, min(ps[3].a-ps[2].a, ps[2].a-ps[1].a)/ps[2].a, (ps[3].a-ps[2].a)/ps[3].a]
    
    for i, t in enumerate(times):
        for j in [1,2,3]:
            a[j,i] = ps[j].a
            e[j,i] = ps[j].e
            inc[j,i] = ps[j].inc
        
        #need to update rhills?
        Rhill12 = ps[1].a*((ps[1].m+ps[2].m)/3.)**(1./3.)
        Rhill23 = ps[2].a*((ps[2].m+ps[3].m)/3.)**(1./3.)
        
        beta12[i] = (ps[2].a - ps[1].a)/Rhill12
        beta23[i] = (ps[3].a - ps[2].a)/Rhill23
        try:
            sim.integrate(t)
        except:
            pass
    
    features = OrderedDict()
    features['t_final_short'] = sim.t/P0
    Ef = sim.calculate_energy()
    features['Rel_Eerr_short'] = abs((Ef-E0)/E0)

    for string, feature in [("beta12", beta12), ("beta23", beta23)]:
        mean = feature.mean()
        std = feature.std()
        features["avg_"+string] = mean
        features["std_"+string] = std
        features["min_"+string] = min(feature)
        features["max_"+string] = max(feature)


    for j in [1,2,3]:
        for string, feature in [('a', a), ('e', e), ('inc', inc)]:
            mean = feature[j].mean()
            std = feature[j].std()
            features['avg_'+string+str(j)] = mean
            features['std_'+string+str(j)] = std
            features['max_'+string+str(j)] = feature[j].max()
            features['min_'+string+str(j)] = feature[j].min()
            features['norm_std_'+string+str(j)] = std/mean
            features['norm_max_'+string+str(j)] = np.abs(feature[j] - mean).max()/mean
            sample = feature[j][:window]
            samplemean = sample.mean()
            features['norm_std_window'+str(window)+'_'+string+str(j)] = sample.std()/samplemean
            features['norm_max_window'+str(window)+'_'+string+str(j)] = np.abs(sample - samplemean).max()/samplemean

        for string, feature in [('eH', e), ('iH', inc)]:
            mean = feature[j].mean()
            std = feature[j].std()
            
            features['avg_'+string+str(j)] = mean/eHill[j]
            features['std_'+string+str(j)] = std/eHill[j]
            features['max_'+string+str(j)] = feature[j].max()/eHill[j]
            features['min_'+string+str(j)] = feature[j].min()/eHill[j]

        string, feature = ('ecross', e)
        features['avg_'+string+str(j)] = mean/daOvera[j]
        features['std_'+string+str(j)] = std/daOvera[j]
        features['max_'+string+str(j)] = feature[j].max()/daOvera[j]
        features['min_'+string+str(j)] = feature[j].min()/daOvera[j]
        
        xx = range(a[j].shape[0])
        yy = a[j]/a[j].mean()/features["t_final_short"]
        par = np.polyfit(xx, yy, 1, full=True)
        features['norm_a'+str(j)+'_slope'] = par[0][0]
    
    t = time.time()
    features['wall_time'] = t-t0

    return pd.DataFrame(features, index=[iteration])

###############################
def system(dir, sim_time, P1, index):
    SA = rebound.SimulationArchive(dir)
    E0 = SA[0].calculate_energy()
    features = generate_features(SA[0], index)
    features['Stable'] = 1 if np.isclose(sim_time/P1, 1e9) else 0
    #print(sim_time/SA[0].particles[1].P, sim_time/P1, features['Stable'].values, dir) #disagreement.. why?
    features['instability_time'] = sim_time
    features['Rel_Eerr'] = abs((SA[-1].calculate_energy()-E0)/E0)
    return features    

from rebound import InterruptiblePool
def dorows(params):
    start, end, df = params
    first = pd.concat([df.iloc[start], system(df.iloc[start])])
    df_full = pd.DataFrame([first])
    for i in range(start+1,end):
        if i == 11003:
            continue
        df_full = df_full.append(pd.concat([df.iloc[i], system(df.iloc[i])]))
        df_full.to_csv('../csvs/tmp/short_integration_features'+str(start)+'.csv', encoding='ascii')

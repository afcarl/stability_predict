import pandas as pd
import numpy as np
import os
import rebound
from collections import OrderedDict

def collision(reb_sim, col):
    reb_sim.contents._status = 5 # causes simulation to stop running and have flag for whether sim stopped due to collision
    return 0

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

def make_sim(d, Ms, epoch):
    sim = rebound.Simulation()
    sim.integrator = 'whfast'
    sim.G = 1
    sim.add(m=Ms)
    
    earth = 0.000003003
    for i in [1,2,3]:
        m, P = d["m%d"%i]*earth*Ms, d["P%d"%i]              # Ms, days
        try:
            e = np.sqrt(d["h%d"%i]**2 + d["k%d"%i]**2)      # sqrt(h^2 + k^2)
            w = np.arctan2(d["h%d"%i],d["k%d"%i])           # arctan2(h/k)
            M = get_M(e,w,d["T%d"%i],P,epoch)               # T = epoch = BJD-2,454,900
        except:
            e = d["e%d"%i]
            w = d["w%d"%i]
            M = d["MA%d"%i]                                 # Mean anomaly
        sim.add(m=m, P=P*2*np.pi/365., e=e, omega=w, M=M)   # G=1 units!
    sim.move_to_com()
    return sim

def generate_features(d, Ms=1, epoch=780):
    # hyperparameters
    maxorbs = 1e4
    Nout = 100
    window = 10
    Navg = 10

    # make sims
    sim = make_sim(d, Ms, epoch)    # primary simulation
    sim2 = make_sim(d, Ms, epoch)   # shadow simulation
    ps = sim.particles

    P0 = ps[1].P
    tmax = maxorbs * P0                 # number of inner planet orbital periods to integrate
    sim.collision_resolve = collision
    sim2.collision_resolve = collision
    sim.dt = P0/20.
    sim2.dt = P0/20.
    
    kicksize=1.e-11
    sim2.particles[2].x += kicksize
    
    E0 = sim.calculate_energy()
    times = np.linspace(0,tmax,Nout)
    
    a = np.zeros((sim.N,Nout))
    e = np.zeros((sim.N,Nout))
    inc = np.zeros((sim.N,Nout))
    e2shadow = np.zeros(Nout)
    
    Rhill12 = ps[1].a*((ps[1].m+ps[2].m)/3.)**(1./3.)
    Rhill23 = ps[2].a*((ps[2].m+ps[3].m)/3.)**(1./3.)
    
    eHill = [0, Rhill12/ps[1].a, max(Rhill12, Rhill23)/ps[2].a, Rhill23/ps[3].a]
    daOvera = [0, (ps[2].a-ps[1].a)/ps[1].a, min(ps[3].a-ps[2].a, ps[2].a-ps[1].a)/ps[2].a, (ps[3].a-ps[2].a)/ps[3].a]

    # simulate primary/shadow systems 
    for i, t in enumerate(times):
        for j in [1,2,3]:
            a[j,i] = ps[j].a
            e[j,i] = ps[j].e
            inc[j,i] = ps[j].inc
        e2shadow[i] = sim2.particles[2].e
        sim.integrate(t)
        sim2.integrate(t)

    features = OrderedDict()
    features['t_final_short'] = sim.t/P0
    Ef = sim.calculate_energy()
    features['Rel_Eerr_short'] = abs((Ef-E0)/E0)

    # make features
    for j in [1,2,3]:
        for string, feature in [('a', a), ('e', e), ('inc', inc)]:
            mean = feature[j].mean()
            std = feature[j].std()
            features['avg_'+string+str(j)] = mean
            features['std_'+string+str(j)] = std
            features['max_'+string+str(j)] = feature[j].max()
            features['min_'+string+str(j)] = feature[j].min()
            features['norm_std_'+string+str(j)] = check_nan(std/mean)
            features['norm_max_'+string+str(j)] = check_nan(np.abs(feature[j] - mean).max()/mean)
            sample = feature[j][:window]
            samplemean = sample.mean()
            features['norm_std_window'+str(window)+'_'+string+str(j)] = check_nan(sample.std()/samplemean)
            features['norm_max_window'+str(window)+'_'+string+str(j)] = check_nan(np.abs(sample - samplemean).max()/samplemean)

        for string, feature in [('eH', e), ('iH', inc)]:
            mean = feature[j].mean()
            std = feature[j].std()

            features['avg_'+string+str(j)] = check_nan(mean/eHill[j])
            features['std_'+string+str(j)] = check_nan(std/eHill[j])
            features['max_'+string+str(j)] = check_nan(feature[j].max()/eHill[j])
            features['min_'+string+str(j)] = check_nan(feature[j].min()/eHill[j])

        string, feature = ('ecross', e)
        features['avg_'+string+str(j)] = check_nan(mean/daOvera[j])
        features['std_'+string+str(j)] = check_nan(std/daOvera[j])
        features['max_'+string+str(j)] = check_nan(feature[j].max()/daOvera[j])
        features['min_'+string+str(j)] = check_nan(feature[j].min()/daOvera[j])

        xx = range(a[j].shape[0])
        yy = a[j]/a[j].mean()/features["t_final_short"]
        par = np.polyfit(xx, yy, 1, full=True)
        features['norm_a'+str(j)+'_slope'] = par[0][0]

    N = min((e[2] > 0).sum(), (e2shadow > 0).sum())                 # Number of nonzero entries in each array, incase they go unstable before sim ends
    Nfit = N//Navg                                                  # N of binned points
    Ntrim = Nfit*Navg                                               # trim array to number that can fit in bins of size Navg
    e2avg = np.average(e[2][:Ntrim].reshape(Nfit, Navg), axis=1)    # reshape into Nfit lists of Navg consecutive values and average
    e2shadowavg = np.average(e2shadow[:Ntrim].reshape(Nfit, Navg), axis=1)
    timesavg = np.average(times[:Ntrim].reshape(Nfit, Navg), axis=1)
    e2diff = np.abs(e2avg - e2shadowavg)
    par = np.polyfit(timesavg, np.log10(e2diff), 1, full=True)
    features['Lyapunov_time'] = 1/par[0][0]
    
    return pd.Series(features, index=list(features.keys()))

#functions below not relevant?#
###############################
def system(row):
    sim = rebound.Simulation.from_file(icpath+row['runstring'])
    E0 = sim.calculate_energy()
    features = generate_features(sim)
    simf = rebound.Simulation.from_file(fcpath+row['runstring'])
    features['Stable'] = 1 if np.isclose(simf.t, 1.e9) else 0
    features['instability_time'] = simf.t
    features['Rel_Eerr'] = abs((simf.calculate_energy()-E0)/E0)
    features.name = row.name
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

#The purpose of this script is to run the jobs generated by "make_Nbody.py". Actual N-body simulations
import pandas as pd
import numpy as np
import os
import sys
import rebound
import time
import math
import systems.sys_params as sysp

# planetary radii are hill radii, and thus if hill radii touch (i.e. collision),
# causes simulation to stop running and have flag for whether sim stopped due to collision
def collision(reb_sim, col):
    reb_sim.contents._status = 5
    return 0

def get_M(e, w, T, P, epoch):
    f_midtr = np.pi/2 - w   #at mid-transit
    E_midtr = 2*np.arctan(np.tan(f_midtr/2) * np.sqrt((1-e)/(1+e))) #E and f always in same half of ellipse
    M_midtr = E_midtr - e*np.sin(E_midtr)
    M_epoch = M_midtr + (epoch - T)*2*np.pi/P
    return M_epoch

#arguments
system = sys.argv[1]
id = int(sys.argv[2])
maxorbs = float(sys.argv[3])
Nplanets = int(sys.argv[4])
shadow = int(sys.argv[5])
name = sys.argv[6]

#load data
data = pd.read_csv('systems/%s_data.csv'%system)
d = data.iloc[id]

#set up simulation
sim = rebound.Simulation()
sim.integrator = 'whfast'
sim.G = 1
sim.ri_whfast.safe_mode = 0
sim.collision = 'direct'
sim.collision_resolve = collision
earth2solar = 0.000003003       # earth to solar mass conversion

#add sun
Ms = d["Ms"]
sim.add(m=Ms)

#add planets
nomass_sys, vaneye_sys, danjh_sys = sysp.get_system_lists()
inc, Omega = [], []
Rs = sysp.get_Rs(system)*0.00465046726  # radius of star in AU
logincmin = np.log10(1.e-3)        # min inclination
for i in range(1, Nplanets + 1):
    m, P = d["m%d"%i]*earth2solar, d["P%d"%i]
    a = ((P/365.)**2 * Ms)**(1./3.)
    if system in nomass_sys:
        e = d["e%d"%i]
        w = d["w%d"%i]
        M = d["MA%d"%i]
    elif system in vaneye_sys:
        e = d["e%d"%i]
        w = d["w%d"%i]
        min_MidTransitTime = np.min((data["T1"], data["T2"], data["T3"]))
        M = get_M(e, w, d["T%d"%i], P, min_MidTransitTime)
    elif system in danjh_sys:
        e = np.sqrt(d["h%d"%i]**2 + d["k%d"%i]**2)      # sqrt(h^2 + k^2)
        w = np.arctan2(d["h%d"%i], d["k%d"%i])          # arctan2(h/k)
        epoch = 780
        M = get_M(e, w, d["T%d"%i], P, epoch)           # T = epoch = BJD-2,454,900
        m *= Ms     # dan jontoff-hutter planetary masses scaled to 1 solar mass.
    else:
        raise Exception('system is not recognized')
        sys.exit(1)
    logincmax = np.log10(0.9*np.arcsin(Rs/a)*np.pi/180) # 0.9 since grazing transits aren't detected
    inc.append(10.**np.random.uniform(logincmin, logincmax))
    Omega.append(2*np.pi*np.random.random())
    hill = a*(m/(3*Ms))**(1./3.)
    sim.add(m=m, a=a, e=e, omega=w, M=M, inc=inc[-1], Omega=Omega[-1], r=hill/2.) # G=1 units!
sim.move_to_com()

#shadow system
if shadow == 1:
    kicksize=1.e-11
    sim.particles[2].x += kicksize

#timestep
dt = 2.*math.sqrt(3)/100.
P1 = sim.particles[1].P
sim.dt = dt*P1              # ~3% orbital period
tmax = maxorbs*P1

#save simulation archive
sim.initSimulationArchive('output/%s_SA_inc.bin'%name, interval=tmax/1000.)     #save checkpoints.

#simulate
E0 = sim.calculate_energy()
t0 = time.time()
print("starting simulation")
sim.integrate(tmax)         # will stop if collision occurs
print("finished simulation")
Ef = sim.calculate_energy()
Eerr = abs((Ef-E0)/E0)

#need to store the result somewhere
f = open('systems/%s_Nbodyresults_inc.csv'%system, "a")
f.write('%s, %d, %d, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e \n'%(name,id,shadow,maxorbs,P1,sim.t,Eerr,time.time()-t0,
                                                                     inc[0],inc[1],inc[2],Omega[0],Omega[1],Omega[2]))

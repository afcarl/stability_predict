import pandas as pd
import numpy as np
import os
import sys
import rebound
import time
import math

def collision(reb_sim, col):
    reb_sim.contents._status = 5 # causes simulation to stop running and have flag for whether sim stopped due to collision
    return 0

def get_M(e, w, T, P, epoch):
    f = np.pi/2 - w
    E = 2*np.arctan(np.tan(f/2) * np.sqrt((1-e)/(1+e))) #E and f always in same half of ellipse
    M = E - e*np.sin(E)
    return M + (epoch - T)*2*np.pi/P

#arguments
id = int(sys.argv[1])
Ms = float(sys.argv[2])
epoch = float(sys.argv[3])
maxorbs = float(sys.argv[4])
shadow = int(sys.argv[5])
name = sys.argv[6]

#load data
system = name.split('_')[0]
data = pd.read_csv('systems/%s_data.csv'%system)
d = data.iloc[id]

#set up simulation
sim = rebound.Simulation()
sim.integrator = 'whfast'
sim.G = 1
sim.ri_whfast.safe_mode = 0
sim.collision = 'direct'
sim.collision_resolve = collision

#add sun
sim.add(m=Ms)

#minimum hill radius
earth = 0.000003003
a1,a2 = ((d["P1"]/365)**2 * Ms)**(1./3.), ((d["P2"]/365)**2 * Ms)**(1./3.)
hill12 = a1*((d["m1"]+d["m2"])*earth/Ms/3.)**(1./3.)
hill23 = a2*((d["m2"]+d["m3"])*earth/Ms/3.)**(1./3.)
minhill = min(hill12,hill23)

#add planets
for i in [1,2,3]:
    e = np.sqrt(d["h%d"%i]**2 + d["k%d"%i]**2)                                      #sqrt(h^2 + k^2)
    w = np.arctan2(d["h%d"%i],d["k%d"%i])                                           #arctan2(h/k)
    m, P, T = d["m%d"%i]*earth/Ms, d["P%d"%i], d["T%d"%i]                           #Ms, days, BJD-2,454,900
    sim.add(m=m, P=P*2*np.pi/365., e=e, omega=w, M=get_M(e,w,T,P,epoch), r=minhill) #G=1 units!
sim.move_to_com()

#shadow system
if shadow == 1:
    kicksize=1.e-11
    sim.particles[2].x += kicksize

#timestep
dt = 2.*math.sqrt(3)/100.
sim.dt = dt*sim.particles[1].P
tmax = maxorbs*sim.particles[1].P

#save simulation archive
sim.save('output/%s_init.bin'%name)                                         #save beginning of sim.
sim.initSimulationArchive('output/%s_SA.bin'%name, interval=tmax/1000.)     #save checkpoints.

#simulate
E0 = sim.calculate_energy()
t0 = time.time()
print "starting simulation"
sim.integrate(tmax)                                                         #will stop if collision occurs
print "finished simulation"
Ef = sim.calculate_energy()
Eerr = abs((Ef-E0)/E0)

#need to store the result somewhere
f = open('systems/%s_Nbodyresults.csv'%system, "a")
f.write('%s, %d, %d, %e, %e, %e, %e \n'%(name,id,shadow,maxorbs,sim.t,Eerr,time.time()-t0))


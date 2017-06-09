#This is just a simple calc to find the hill separations between planetary systems.

import numpy as np

#**************************Systems**************************
#Kepler-114 (KOI-156)
#name = "Kepler-114"
#P = [5.1885,8.0413,11.7761]     #days
#r = [1.26,1.60,2.53]            #Earth-radii
#m,a = [],[]
#Ms = 0.56

#Kepler-81 (KOI-877)
#name = "Kepler-81"
#P = [5.955,12.040,20.83]        #days
#r = [2.42,2.37,1.21]            #Earth-radii
#m,a = [],[]
#Ms = 0.64

#Kepler-54 (KOI-886)
#name = "Kepler-54"
#a = [0.111,0.281,0.392]         #AU
#r = [1.19,3.38,2.47]            #Earth-radii
#m = []
#Ms = 0.85

#Kepler-359 (KOI-2092)
#name = "Kepler-359"
#a = [0.178,0.307,0.372]         #AU
#r = [3.53,4.30,4.01]            #Earth-radii
#m = []
#Ms = 1.07

#Kepler-372 (KOI-2195)
#name = "Kepler-372"
#a = [0.075,0.154,0.201]         #AU
#r = [1.36,2.09,1.69]            #Earth-radii
#m = []
#Ms = 1.15

#Kepler-18 (KOI-137)
#name = "Kepler-18"
#a = [0.0447,0.0752,0.1172]         #AU
#r = [2,5.49,6.98]            #Earth-radii
#m = []
#Ms = 0.972

#Kepler-60 (KOI-2086)
#name = "Kepler-60"
#P = [7.1334,8.92,11.898]         #AU
#m = np.asarray([0.0132,0.0121,0.0131])*0.0009543
#a = []
#Ms = 1.041

#Kepler-65 (KOI-85)
#name = "Kepler-65"
#a = [0.035,0.068,0.084]         #AU
#r = [1.42,2.58,1.52]            #Earth-radii
#m = []
#Ms = 1.25

#Kepler-23 (KOI-168)
#name = "Kepler-23"
#a = [0.075, 0.099, 0.124]       #AU
#r = [1.9,3.2,2.2]               #Earth-radii
#m, P = [], []
#Ms = 1.11

#Kepler-149 (KOI-401)
#name = "Kepler-149"
#a = [0.184, 0.281, 0.571]       #AU
#r = [4.21,1.61,3.96]            #Earth-radii
#m, P = [], []
#Ms = 0                         #unknown value

##Kepler-51 (KOI-620)
#name = "Kepler-51"
#a = [0.2514, 0.384, 0.509]       #AU
#m = np.asarray([0.007,0.013,0.024])*0.0009543
#Ms = 1.04

#Kepler-30 (KOI-806)
#name = "Kepler-30"
#a = [0.18, 0.30, 0.50]       #AU
#m = np.asarray([0.036,2.01,0.073])*0.0009543
#Ms = 0.99

#HD 7924
name = "HD 7924"
a = [0.05664,0.1134,0.1551]
m = np.asarray([0.0273,0.0247,0.0203])*0.0009543    #Jupiter mass->Solar mass
Ms = 0.832
#**************************Systems**************************

#constants
rho_E = 5515.3      #density Earth in kg/m^3
rho_N = 1638        #density of Neptune in kg/m^3
r2m = 6371000       #radius of earth (meters)
msun = 1.989*10**30 #mass of sun (kg)

if Ms == 0:
    print "stellar mass unknown, setting to 1"
    Ms = 1.0

if len(m)==0 and len(r)>0:
    print "masses not provided, converting radius to masses..."
    for rp in r:
        if rp > 1.6:
            rho = rho_N
        else:
            rho = rho_E
        mass = rho*(4./3.)*np.pi*(rp*r2m)**3 / msun
        m.append(mass)

if len(a)==0 and len(P)>0:
    print "semi-major axis not provided, converting periods..."
    P = np.asarray(P)
    a = ((P/365)**2 * Ms)**(1./3.)

#hill radii
RH = []
for i in range(len(a)-1):
    hill = a[i]*((m[i] + m[i+1])/(3*Ms))**(1./3.)
    RH.append(hill)

#separations
print ""
print "%s:"%name
for i in range(len(a)-1):
    asep = (a[i+1] - a[i]) /RH[i]
    print "Planets %d and %d are separated by %f mutual Hill radii"%(i+1, i, asep)

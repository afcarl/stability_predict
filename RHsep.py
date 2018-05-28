#This is just a simple calc to find the hill separations between planetary systems.
#The separations of interest are < 30.

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
#P = [7.1334,8.92,11.898]         #days
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
#name = "HD 7924"
#a = [0.05664,0.1134,0.1551]
#m = np.asarray([0.0273,0.0247,0.0203])*0.0009543    #Jupiter mass->Solar mass
#Ms = 0.832

################Suvrath/Gummi################
#name = "EPIC 210897587"
#P = [6.3441,13.86,40.68]
#r = [1.55,1.95,1.64]
#m,a = [],[]
#Ms = 0.540

#name = "KOI-94"
#P = [3.74, 10.42, 22.34, 54.32]
##r = [1.55,1.95,1.64]
#m = [10.5*3e-6, 15.6*3e-6, 106*3e-6, 35*3e-6]
#a = []
#Ms = 0.540

name = "sample"
#P = [1, 1.82, 3.5, 6.7]
#m = [15*3e-6, 15*3e-6, 15*3e-6, 15*3e-6]
P = [1, 1.94, 4.35, 9.82]
m = [3e-6*.0363, 3e-6*11.6, 3e-6*29.2, 3e-6*29.9]
a = []
Ms = 1

################Perfect test systems################
#Kepler-431
#name = "Kepler-431"
#P = [6.803,8.703,11.922]
#r = [0.764,0.668,1.11]
#m,a = [], []
#Ms = 1.071

#LP 358-499
#name = "LP 358-499"
#r = [1.38, 1.56, 2.12]          #Earth-radii
#a = [0.0333, 0.0452, 0.078]    #AU
#P = [3.0711, 4.8682, 11.0235]  #days
#m = []
#Ms = 0.52

#GJ 9827
#name = "GJ 9827"
#P = [1.2,3.6,6.2]
#r = [1.64,1.29,2.08]
#m,a = [], []
#Ms = 0.659

#Kepler-446 (Kepler-445 also works) - authors fixed eccentricity to 0 in fit.
#name = "Kepler-446"
#P = [1.565409, 3.036179, 5.148921]
#r = [1.50,1.11,1.35]
#m, a = [], []
#Ms = 0.22

################Van Eylen Systems################
#Kepler-92 (KOI-285)
#name = "Kepler-92"
#P = [13.749,26.723,49.357]      #days
#r = [3.65, 2.455, 2.067]        #Earth radii
#a, m = [], []                   #masses exist for inner two planets, Xie (2014)
#Ms = 1.209

#Kepler-127 (KOI-271) - Hill separations are 33 and 20
#name = "Kepler-127"
#P = [14.44, 29.39, 48.63]     #days
#r = [1.52, 2.389, 2.668]       #Earth radii
#a, m = [], []
#Ms = 1.240

#Kepler-450 (KOI-279) - Hill separations are 37 and 13
#name = "Kepler-450"
#P = [7.515, 15.413, 28.454]     #days
#r = [0.837, 2.62, 6.14]         #Earth radii
#a, m = [], []
#Ms = 1.346

#Kepler-100 (KOI-41) - Hill separations are 30 and 52, too large
#name = "Kepler-100"
#P = [6.887, 12.816, 35.333]     #days
#r = [1.305, 2.221, 1.514]       #Earth radii
#a, m = [], []
#Ms = 1.109

#Kepler-126 (KOI-260) - Hill separations are 35 and 91, too large
#name = "Kepler-126"
#P = [10.49, 21.870, 100.282]     #days
#r = [1.439, 1.498, 2.513]       #Earth radii
#a, m = [], []
#Ms = 1.148

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
Np = len(a)
RHmut, RH = np.zeros((Np,Np)), []
for i in range(Np-1):
    RH.append(a[i]*(m[i]/(3*Ms))**(1./3.))
    for j in range(i+1,Np):
        RHmut[i][j] = 0.5*(a[i]+a[j])*((m[i] + m[j])/(3*Ms))**(1./3.)

#separations
print ""
print "%s:"%name
for i in range(Np-1):
    for j in range(i+1, Np):
        asep = (a[j] - a[i]) /RHmut[i][j]
        asep2 = (a[j] - a[i]) /RH[i]
        if len(P) > 0:
            print "Planets %d and %d are separated by %f mutual Hill radii, with a period ratio of %f"%(j, i, asep, P[j]/P[i])
        else:
            print "Planets %d and %d are separated by %f mutual Hill radii"%(j, i, asep)

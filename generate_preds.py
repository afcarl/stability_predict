# The purpose of this code is to generate predictions from the data so that we can ultimately compare to the Nbody results

import dill
import rebound
import numpy as np
import pandas as pd
import run_Nbody_inc as Nbod

def stable(sim):
    try:
        prob = model.predict_proba(feature_function(sim)[features])[0][1]
    except:
        prob = 0
    return prob

########################
system = "Kepler-431"
shadow = 0
data = pd.read_csv("systems/%s_data.csv"%system)
Nbodydata = pd.read_csv("systems/%s_Nbodyresults_inc.csv"%system,
                        names=["name","id","shadow","maxorbs","P1","sim.time","Eerr",
                               "CPU.time","inc1","inc2","inc3","Omega1","Omega2","Omega3"])
model, features, feature_function = dill.load(open("models/ApplicationsModel_Feb2018dill.pkl", "rb"))

prob = []
for id, row in data[0:2].iterrows():
    NBD = Nbodydata[(Nbodydata["id"]==id)&(Nbodydata["shadow"]==shadow)]
    inc = [NBD["inc1"].values, NBD["inc2"].values, NBD["inc3"].values]
    Omega = [NBD["Omega1"].values, NBD["Omega2"].values, NBD["Omega3"].values]
    sim = Nbod.make_sim(row, system, inc, Omega)
    print(sim.status())
    p = model.predict_proba(feature_function(sim)[features])[0][1]
    prob.append(p)

print(prob)

# The purpose of this code is to generate predictions from the data so that we can ultimately compare to the Nbody results

import pickle
import rebound
import numpy as np
import pandas as pd
import run_Nbody_inc as Nbod
import generatefeatures as gen
import xgboost as xgb

#########Parameters#########
system = "Kepler-431"
dir_SA = "simulation_archives/%s_inc"%system   #ACI-b
#dir_SA = "simulation_archives"
shadow = 0
############################

# model and data
model = pickle.load(open("models/final_Naireen2018.pkl", "rb"))
#data = pd.read_csv("systems/%s_data.csv"%system)
Nbodydata = pd.read_csv("systems/%s_Nbodyresults_inc.csv"%system,
                        names=["name","id","shadow","maxorbs","P1","sim.time","Eerr",
                               "CPU.time","inc1","inc2","inc3","Omega1","Omega2","Omega3"])

model_features = ['avg_iH1', 'avg_iH2', 'norm_std_a1', 'norm_max_a1', 'norm_std_window10_a1', 'norm_max_window10_a1',
            'norm_std_a2', 'norm_max_a2', 'norm_std_window10_a2', 'norm_max_window10_a2','norm_std_a3',
            'norm_max_a3', 'norm_std_window10_a3', 'norm_max_window10_a3', 'avg_ecross1', 'std_ecross1',
            'max_ecross1', 'min_ecross1', 'avg_ecross2', 'std_ecross2', 'max_ecross2', 'min_ecross2',
            'avg_ecross3', 'std_ecross3', 'max_ecross3', 'min_ecross3', 'norm_a1_slope', 'norm_a2_slope',
            'norm_a3_slope', 'avg_beta12','std_beta12','min_beta12','max_beta12','avg_beta23','std_beta23',
            'min_beta23','max_beta23']

try:
    df = pd.read_csv('systems/%s_preds_inc.csv'%system)
except:
    # make data frame
    df = pd.DataFrame(columns=model_features)
    for index, row in Nbodydata.iterrows():
        try:
            dir_sim = '%s/%s_SA_inc.bin'%(dir_SA, row['name'])
            features = gen.system(dir_sim, row['sim.time'], row['P1'], index)
            df = pd.concat([df, features[model_features]])
        except:
            pass
        df.to_csv('systems/%s_preds_inc.csv'%system)

X = xgb.DMatrix(df[model_features])
preds = model.predict(X)
print(preds)

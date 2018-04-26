# This script generates predictions straight from the Simulation Archives, no Nbody csv files.

import pickle
import rebound
import numpy as np
import pandas as pd
import glob
import run_Nbody_inc as Nbod
import utils.generatefeatures as gen
import xgboost as xgb
import os

model_features = ['avg_iH1', 'avg_iH2', 'norm_std_a1', 'norm_max_a1', 'norm_std_window10_a1',
                  'norm_max_window10_a1','norm_std_a2', 'norm_max_a2', 'norm_std_window10_a2',
                  'norm_max_window10_a2','norm_std_a3','norm_max_a3', 'norm_std_window10_a3',
                  'norm_max_window10_a3', 'avg_ecross1', 'std_ecross1','max_ecross1', 'min_ecross1',
                  'avg_ecross2', 'std_ecross2', 'max_ecross2', 'min_ecross2','avg_ecross3',
                  'std_ecross3', 'max_ecross3', 'min_ecross3', 'norm_a1_slope', 'norm_a2_slope',
                  'norm_a3_slope', 'avg_beta12','std_beta12','min_beta12','max_beta12','avg_beta23',
                  'std_beta23','min_beta23','max_beta23']

############################
def get_features(system, dir_SA):

    try:
        df = pd.read_csv('systems/%s_features.csv'%system)
        print('***Loaded predictions for system %s.'%system)
    except:
        SAs = glob.glob("%s*_SA.bin"%dir_SA)
        
        # make data frame
        print('***Couldnt retrieve predictions for system %s, generating from scratch***'%system)
        mf = list(model_features)  # copy
        mf += ['name','id']
        df = pd.DataFrame(columns=mf)
        for dir_sim in SAs:
            basename = os.path.basename(dir_sim.split('_SA.bin')[0])
            dir_final = basename + '_final.bin'
            P1 = rebound.SimulationArchive(dir_sim)[0].particles[1].P
            sim_time = rebound.SimulationArchive(dir_final)[-1].t
            try:
                features = gen.system(dir_sim, sim_time, P1, index)[model_features]
                features['name'] = basename
                features['id'] = basename.split('_')[-1]
                df = pd.concat([df, features])
            except:
                pass
        df.to_csv('systems/%s_features%s.csv'%(system, ext))
    return df

#########Parameters#########
if __name__ == "__main__":
    #    systems = ["Kepler-431","Kepler-446","KOI-0085","KOI-0115","KOI-0156",
    #               "KOI-0168","KOI-0250","KOI-0314","KOI-1576","KOI-2086","LP-358-499"]
    systems = ["Ari_Fake_10_0.1_r1/"]
    ext = "_SA"
    model = pickle.load(open("models/final_Naireen2018.pkl", "rb"))
    
    for system in systems:
        dir_SA = "/storage/work/cjg66/ML-Stability/output/Ari_Fake_10_0.1_r1/%s"%system   #ACI-b
        
        df = get_features(system, dir_SA)
        X = xgb.DMatrix(df[model_features])
        preds = model.predict(X)
        print(system)
        print(preds)

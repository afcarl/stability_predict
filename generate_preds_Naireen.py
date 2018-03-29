# The purpose of this code is to generate predictions from the data so that we can ultimately compare to the Nbody results

import pickle
import rebound
import numpy as np
import pandas as pd
import run_Nbody_inc as Nbod
import generatefeatures as gen
import xgboost as xgb

model_features = ['avg_iH1', 'avg_iH2', 'norm_std_a1', 'norm_max_a1', 'norm_std_window10_a1',
                  'norm_max_window10_a1','norm_std_a2', 'norm_max_a2', 'norm_std_window10_a2',
                  'norm_max_window10_a2','norm_std_a3','norm_max_a3', 'norm_std_window10_a3',
                  'norm_max_window10_a3', 'avg_ecross1', 'std_ecross1','max_ecross1', 'min_ecross1',
                  'avg_ecross2', 'std_ecross2', 'max_ecross2', 'min_ecross2','avg_ecross3',
                  'std_ecross3', 'max_ecross3', 'min_ecross3', 'norm_a1_slope', 'norm_a2_slope',
                  'norm_a3_slope', 'avg_beta12','std_beta12','min_beta12','max_beta12','avg_beta23',
                  'std_beta23','min_beta23','max_beta23']

############################
def get_features(system, dir_SA, ext):
    #data = pd.read_csv("systems/%s_data.csv"%system)
    Nbodydata = pd.read_csv("systems/%s_Nbodyresults_inc.csv"%system,
                            names=["name","id","shadow","maxorbs","P1","sim_time","Eerr",
                                   "CPU_time","inc1","inc2","inc3","Omega1","Omega2","Omega3"])
                                   
    try:
        df = pd.read_csv('systems/%s_features_inc.csv'%system)
        print('***Loaded predictions for system %s.'%system)
    except:
        # make data frame
        print('***Couldnt retrieve predictions for system %s, generating from scratch***'%system)
        mf = list(model_features)  # copy
        mf += ['name','id','shadow']
        df = pd.DataFrame(columns=mf)
        for index, row in Nbodydata.iterrows():
            try:
                dir_sim = '%s/%s_SA_inc.bin'%(dir_SA, row['name'])
                features = gen.system(dir_sim, row['sim.time'], row['P1'], index)[model_features]
                features['name'] = row['name']
                features['id'] = row['id']
                features['shadow'] = row['shadow']
                df = pd.concat([df, features])
            except:
                pass
            df.to_csv('systems/%s_features%s.csv'%(system, ext))
    return df

#########Parameters#########
if __name__ == "__main__":
    systems = ["Kepler-431","Kepler-446","KOI-0085","KOI-0115","KOI-0152","KOI-0156",
               "KOI-0168","KOI-0250","KOI-0314","KOI-1576","KOI-2086","LP-358-499"]
    model = pickle.load(open("models/final_Naireen2018.pkl", "rb"))
    ext = "_inc"    # ext can be '_inc' or ''

    for system in systems:
        dir_SA = "simulation_archives/%s%s"%(system, ext)   #ACI-b
        #dir_SA = "simulation_archives"
        
        df = get_features(system, dir_SA, ext)
        X = xgb.DMatrix(df[model_features])
        preds = model.predict(X)
        print(system)
        print(preds)


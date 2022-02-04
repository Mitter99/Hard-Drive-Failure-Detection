import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import time
import warnings
import joblib

from sklearn.model_selection import train_test_split
import math

import lightgbm as lgb
from datetime import datetime,timedelta
from tqdm import tqdm
from sklearn.metrics import roc_curve, auc, f1_score, accuracy_score, precision_score, recall_score, roc_auc_score


def data_cleaning(df):
    #df['capacity_tb']=df['capacity_bytes']/1e12
    #df=df.drop(['capacity_bytes'],axis=1)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df_fail= df[df['failure']==1]
    df_run= df[df['failure']==0]
    
    df_wf = df.loc[df['serial_number'].isin(df_fail['serial_number'])]
    df_wf= df_wf[df_wf['failure']==0]
    
    
    for ind in tqdm(df_fail.index):
        for j in df_wf.index:
            if (df_fail['serial_number'][ind]== df_wf['serial_number'][j]) and \
             ((df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=1))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=2))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=3))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=4))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=5))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=6))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=7))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=8))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=9))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=10))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=11))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=12))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=13))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=14))) or \
              (df_wf['date'][j]== (df_fail['date'][ind]-timedelta(days=15)))):
                 
            #print(df_fail['serial_number'][ind])
                df_wf.at[j,'failure']=1
            
            
    df_hf= df_wf[df_wf['failure']==1]
    fail=[df_fail,df_hf]
    df_15= pd.concat(fail)
    
    df_nf= df_wf[df_wf['failure']==0]
    df_ran= df_nf.sample(len(df_15))
    d=[df_15,df_ran]
    data= pd.concat(d)
    
    return data
        

def model_fitting(test):
    
    df= pd.read_csv('pre_feat.csv')
    data= data_cleaning(df)
    y= data['failure']
    X= data[['smart_5_raw','smart_9_raw','smart_187_raw','smart_188_raw','smart_193_raw','smart_194_raw','smart_197_raw','smart_198_raw','smart_241_raw','smart_242_raw']]
    
    clf= lgb.LGBMClassifier(learning_rate=0.3, n_estimators=500)
    clf.fit(X,y)
    
    model_save= joblib.dump(clf,'final_model.pkl')
    pred= clf.predict(test)
    return pred


def final_fun_1():

    test=[[168.0,22293.0,0.0,0.000000e+00,85.0,23.0,0.0,0.0,5.839854e+10,1.923334e+11]]
    #2020-01-01,ZA153S5V,ST8000NM0055,8001563222016,1,168.0,22293.0,0.0,0.000000e+00,85.0,23.0,0.0,0.0,5.839854e+10,1.923334e+11
    result= model_fitting(test)
    if result==0:
        print('Hard Disk: Fail')
    else:
        print('Hard Disk: Running')
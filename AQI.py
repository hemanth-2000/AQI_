# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 21:11:39 2021

@author: hemua
"""

import pandas as pd
import numpy as np
import os
import time
import requests
import sys
import datetime as dt


def concat():
    list =[]
        
    for subdir, dirs, files in os.walk('Data\Html_Data'):
        
        if subdir==r'Data\Html_Data\2020':
            break
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith(".html"):
            
                list.append(filepath)
            
    
    df = pd.DataFrame(columns=('T', 'TM', 'Tm','SLP', 'H', 'VV', 'V', 'VM'))
    
    for i in list:
        path = i
        table1 = pd.read_html(path,header=None)
        table1=table1[2]
        table1 = table1.iloc[:-2].drop(['Day','PP','VG','RA','SN','TS','FG'],axis=1)
    
        df = pd.concat([df,table1],ignore_index=True)
    return df

def combine():
    aqi=pd.read_csv('Data\AQI\city_hour.csv')
    aqi = aqi.loc[aqi['City'].str.contains("Delhi", case=False)]
    aqi=aqi[["PM2.5","Datetime"]]
    aqi = aqi[aqi['Datetime']<'2020-01-01 01:00:00']
    aqi.fillna(0,inplace=True)
    aqi.drop(['Datetime'],axis=1,inplace=True)
    aqi.reset_index(drop=True,inplace=True)
    N = 24
    aqi=aqi.groupby(aqi.index // N).sum()/24
    return aqi

def test_data():
    list =[]
        
    for subdir, dirs, files in os.walk('Data\Html_Data'):
        
        if subdir==r'Data\Html_Data\2020':
            
            for filename in files:
                filepath = subdir + os.sep + filename

                if filepath.endswith(".html"):
            
                    list.append(filepath)
                
                
    
    df1 = pd.DataFrame(columns=('T', 'TM', 'Tm','SLP', 'H', 'VV', 'V', 'VM'))
    
    for i in list:
        path = i
        table2 = pd.read_html(path,header=None)
        table2=table2[2]
        table2 = table2.iloc[:-2].drop(['Day','PP','VG','RA','SN','TS','FG'],axis=1)
    
        df1 = pd.concat([df1,table2],ignore_index=True)
    return df1 
    
    
if __name__=="__main__":
    climate=concat()
    aqi_value=combine()
    final=pd.concat([climate,aqi_value],axis=1)
    final=final.replace("-",np.NaN)
    final.dropna(inplace=True)
    final.reset_index(drop=True, inplace=True)
    final.to_csv('Data/combined-Data/final.csv',index=False)
    test=test_data()
    test=test.replace("-",np.NaN)
    test.dropna(inplace=True)
    test.reset_index(drop=True, inplace=True) 
    test.to_csv('Data/combined-Data/test-data.csv',index=False)

    


        


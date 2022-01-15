# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 05:03:20 2022

@author: dhiraj
"""


from flask import Flask,request
import pandas as pd
import numpy as np
import pickle
import flasgger
from flasgger import Swagger


app=Flask(__name__)

Swagger(app)


pickel_in=open('knnModel.pkl','rb')
model1=pickle.load(pickel_in)


@app.route('/')
def welcome():
    return "Welcome to All !!!"

@app.route('/predict',methods=["Get"])
def predict_litho_level():
    """Let's Predict the Lithology Level from Well Log Data 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: RHOB
        in: query
        type: number
        required: true
      - name: NPHI
        in: query
        type: number
        required: true
      - name: GR
        in: query
        type: number
        required: true
      - name: DTC
        in: query
        type: number
        required: true
      - name: DTS
        in: query
        type: number
        required: true
       
    responses:
        200:
            description: The output values
        
    """
    
    
    #DEPTH_MD=request.args.get('DEPTH_MD')
    #CALI=request.args.get('CALI')
    #RSHA=request.args.get('RSHA')
    #RMED=request.args.get('RMED')
    #RDEP=request.args.get('RDEP')
    ###
    RHOB=request.args.get('RHOB')
    NPHI=request.args.get('NPHI')
    GR=request.args.get('GR')
    DTC=request.args.get('DTC')
    DTS=request.args.get('DTS')
    
    ##
    #PEF=request.args.get('PEF')
    
    #SP=request.args.get('SP')
    #BS=request.args.get('BS')
    #skewness=request.args.get("skewness")
    
    prediction=model1.predict([[RHOB,NPHI,GR,DTC,DTS]])
    #print(prediction)
    #########
    lithoDic={"[0]": 'Sandstone',
                 "[1]": 'Shale',
                 "[2]": 'Limestone',
                 "[3]": 'coal',
                 }
    
    pred=str(prediction)
    print(pred)
    ans=lithoDic.get(pred)
    print(ans)
    
    return "The Predicted Lithogy Key Value is:"+ str(pred)+"and Litho Type is:"+str(ans)

@app.route('/predict_file',methods=["POST"])
def predict_litho_level_file():
    """Let's Predict the Lithology Level from Well Log Data 
    This is using docstrings for specifications.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: The output values
        
    """
    
    
    df_test=pd.read_csv(request.files.get("file"))
    print(df_test.head())
    prediction=model1.predict(df_test)
    
    return "The predicted values for the csv file is:"+ str(list(prediction))




if __name__=='__main__':
    app.run()
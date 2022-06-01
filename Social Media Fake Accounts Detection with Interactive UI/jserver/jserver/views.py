from django.shortcuts import render
from django.http import JsonResponse
import json
import pandas as pd
import joblib
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
import numpy as np
from keras.models import load_model

model = joblib.load('finalmodel.pkl')

def scoreJson(request):
    print(request.body)
    # score=float(score)
    data =json.loads(request.body)
    dataF=pd.DataFrame({'x':data}).transpose()
    score=model.predict_proba(dataF)[:,-1][0]
    score=float(score)

# "24","4","588","16","0","Thu Sep 08 13:20:35 +0000 2011",,"en",,,,,,"http://a0.twimg.com/profile_images/3146805145/76be8b13af1031d56b16314829900c5f_normal.jpeg","https://twimg0-a.akamaihd.net/profile_banners/370098498/1358837750","1","https://twimg0-a.akamaihd.net/profile_background_images/770068140/f9fc87593d52e757ce86478b78580894.jpeg","333333","https://twimg0-a.akamaihd.net/profile_images/3146805145/76be8b13af1031d56b16314829900c5f_normal.jpeg","FFFFFF",,"DDEEF6","http://a0.twimg.com/profile_background_images/770068140/f9fc87593d52e757ce86478b78580894.jpeg","C6E2EE","1F98C7",,,,,"2015-02-14 10:40:01","INT"
    return JsonResponse({'score':score})


def scoreFile(request):
    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    filePath='.'+filePathName

    data =pd.read_csv(filePath)
    score=model.predict_proba(data)[:,-1]

    score={j:k for j,k in zip(data['Loan_ID'],score)}

    score =sorted(score.items(),key=lambda x: x[1],reverse=True)

    return JsonResponse({'result':score})

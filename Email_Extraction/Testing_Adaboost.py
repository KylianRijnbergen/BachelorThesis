# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 14:45:59 2020

@author: Kylian Rijnbergen
"""

import pandas as pd
import DataFrameFunctions as DfFun
from sklearn.model_selection import train_test_split
import numpy as np 
from sklearn.ensemble import AdaBoostClassifier
from sklearn import metrics


Directory_Labelled_Emails = "D:/Bachelor_Thesis/Email_Extraction/"
List_Mail_Files =  ["Raw_Data_Csv_File_Raw_Data_Csv_File_Debugging_File_100_Rows_Only_05_07_2020_15_12_07_05_07_2020_15_14_23"]	

Df_Data = pd.DataFrame()
#Load files and add contents to Pandas Dataframe "Df_Raw_Data".
for Filename in List_Mail_Files:
    with open(Directory_Labelled_Emails + Filename + ".csv") as File_To_Load:
        Df_Raw_File_Data = pd.read_csv(File_To_Load)
        Df_Data = Df_Data.append(Df_Raw_File_Data)
    del Df_Raw_File_Data


  
del Directory_Labelled_Emails
del Filename
del List_Mail_Files

Np_Data = Df_Data.to_numpy()
Np_New_Data = np.delete(Np_Data, [0, 1, 4], axis = 1)

Labels = DfFun.GetColumnFromDataFrame(Df_Data, "Label")
Np_Labels = Labels.to_numpy()

Accuracy = 0

Start = 0
End = 100

#Not working for random state 231. 165 takes longer..

for index in range(Start, End):
    print(index)
    X_train, X_test, y_train, y_test = train_test_split(Np_New_Data, Np_Labels, test_size = 0.2, random_state = index)
    abc = AdaBoostClassifier(n_estimators=5, learning_rate=1)
    abc.fit(X_train, y_train.ravel())
    y_pred = abc.predict(X_test)
    ThisAccuracy = metrics.accuracy_score(y_test, y_pred)
    Accuracy = Accuracy + ThisAccuracy
    del abc
    
print("Accuracy:" + str(Accuracy / (End - Start)))
